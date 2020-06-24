from datetime import datetime
import logging
import argparse

import app.application.db as db

from numpy import percentile, median
import math
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


logger = logging.getLogger(__name__)


def get_estrategia(estrategia):
    mp = {"ev_ebit_roic": ("EVSobreEBIT", "ROIC",),
          "pl_roe": ("precoSobreLucro", "ROE",)}
    return mp[estrategia]


def stocks_list(estrategia, valor, liquidez_media_minima=1000000):
    data = db.consulta_detalhes("financial")

    df = pd.DataFrame(data)
    df.set_index("code")
    df = df[ (df.liquidezMediaDiaria > liquidez_media_minima) & \
             (df.margemLiquida >= 7) & \
             (df[valor] > 0) ]

    # Essas métricas não funcionam para instituições financeiras
    if estrategia == "ev_ebit_roic":
        df = df[ (df.setor != "Financeiro e Outros") ]

    return df


def get_result(estrategia):
    valor, performance = get_estrategia(estrategia)

    df = stocks_list(estrategia, valor)
    valor_ordered = df.sort_values(by=[valor])['code'][:150].values
    performance_ordered = df.sort_values(by=[performance], ascending=False)['code'][:150].values

    ranking = pd.DataFrame()
    ranking['position'] = range(1, valor_ordered.size + 1)
    ranking[valor] = valor_ordered
    ranking[performance] = performance_ordered

    valor_list = ranking.pivot_table(columns=valor, values='position')
    performance_list = ranking.pivot_table(columns=performance, values='position')
    concatenado = pd.concat([valor_list, performance_list])

    rank = concatenado.dropna(axis=1).sum()
    rank_sorted = rank.sort_values()[:50]

    rank_validated = []
    for code, score in rank_sorted.iteritems():
         if valida_empresa(code):
            rank_validated.append([score, code])

    return rank_validated


def safe_div(n, d):
    try:
        r = n / d
    except ZeroDivisionError:
        return 0
    return r


def valida_ultimos_lucros(lucros, ultimos_12m):
    """
    Verifica se os últimos resultados foram positivos
    """
    # os 2 ultimos anos descartando o ultimo
    data_p = sorted(lucros.items(), key=lambda item: item[0], reverse=True)[:2]

    status = True

    # verificar os ultimos anos se tem prejuizo
    count = 0
    for v in data_p:
        vlr = v[1]

        if vlr < 0:
            count += 1

    if count > 0:
        logger.info(f"{count} anos com prejuízo")
        status = False

    # os ultimos 3 anos a partir do primeiro
    # verifica se os lucros vem caindo
    lucros_desc, ctrl = 0, 0
    if count == 0:
        data_l = sorted(lucros.items(), key=lambda item: item[0], reverse=False)[-3:]

        ultimo_lucro, ctrl = None, 0
        for v in data_l:
            vlr = v[1]
            ctrl += 1

            # verifica se o lucro vem caindo
            if ultimo_lucro:
                # ex: se 2018 for menor que 2017 (gordura de 15%)
                if vlr < (ultimo_lucro * 0.85):
                    lucros_desc += 1
                    ultimo_lucro = vlr
            else:
                ultimo_lucro = vlr

        # se tem muitos lucros descrescentes
        if lucros_desc == (ctrl - 1):
            status = False
            logger.info(f"{lucros_desc} lucros decrescendo")

        # veririca se o lucro dos ultimos 12m é abaixo do p70 dos ultimos 2 anos fechados
        ptl = percentile(data_l[-2:], 62)
        if ultimos_12m < ptl:
            status = False
            logger.info(f"Descartando pois lucros de 12m com {ultimos_12m} e p70 {ptl}")

    return status


def lucro_resultado_geral(data, media):
    # se p50 for menor que zero ou media menor que zero
    p50 = percentile([x for x in data.values()], 50)
    if p50 < 0:
        logger.info(f"Lucro p50 abaixo de zero {p50}")
        return False
    elif media < 0:
        logger.info(f"Média lucros geral abaixo de zero {media}")
        return False
    return True


def valida_empresa(code):
    lc, media, ultimos_12m = get_lucro_details(code)

    status = valida_ultimos_lucros(lc, ultimos_12m)
    if not status:
        logger.info(f"Descartando {code} pelos últimos lucros")

    if status:
        # somente valida o geral se os ultimos forem positivos
        status = lucro_resultado_geral(lc, media)
        if not status:
            logger.info(f"Descartado {code} pelos lucros históricos negativos")

    return status


def get_lucro_details(code):
    details = db.consulta_detalhes("dre", code)

    lc = {}
    ultimos_12m = None
    for row in details[0]:
        if row["tipo"] == "Lucro Líquido - (R$)":
            periodo = row["periodo"]
            lucro = row["valor"]
            if periodo == "Últ. 12M":
                ultimos_12m = lucro
            else:
                lc[int(periodo)] = float(lucro)

    values = [x for x in lc.values()]
    media = safe_div(sum(values), len(values))

    return lc, media, ultimos_12m


def check_dre(code):
    """
    Aqui podem ser inseridos outros dados como receita, lucros, etc
    """
    dre = {}
    dre["lucro"], dre["media_lucro"], dre["lucro_12m"] = get_lucro_details(code)

    return dre


def millify(n):
    millnames = ["", " Mil", " Mi", " Bi", " Tri"]

    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )
    result = n / 10 ** (3 * millidx), millnames[millidx]

    return "{:.1f}{}".format(result[0], result[1])


def format_number(n, repl="-"):
    if n:
        return round(n, 2)
    return repl


def rank(estrategia):
    log = "Iniciando a análise "
    if estrategia == "ev_ebit_roic":
        log += "usando a estratégia EV/EBIT e ROIC "
    else:
        log += "usando a estratégia P/L e ROE "
    logger.info(log)

    magic_result = get_result(estrategia)
    return magic_result


def columns():
    return [
        {"text": "score", "type": "number"},
        {"text": "code", "type": "string"},
    ]
