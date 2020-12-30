import logging

from app.application import db

from numpy import percentile
import warnings

warnings.filterwarnings("ignore")


logger = logging.getLogger(__name__)


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

    # verificar os ultimos anos se vem tendo prejuizo
    for v in data_p:
        vlr = v[1]
        if vlr < 0:
            logger.info(f"Prejuízo nos últimos 2 anos - {data_p}")
            return False

    # os ultimos 3 anos a partir do primeiro
    # verifica se os lucros vem caindo
    data_l = sorted(lucros.items(), key=lambda item: item[0], reverse=False)[-3:]
    lucros = [v[1] for v in data_l]

    # adiciona o vlr dos ultimos 12m
    lucros.append(ultimos_12m)

    ultimo_lucro, ctrl = None, 0
    lucros_desc, ctrl = 0, 0
    for l in lucros:
        ctrl += 1

        # verifica se o lucro vem caindo
        if ultimo_lucro:
            # ex: se 2018 for menor que 2017 (gordura de x%)
            if l < (ultimo_lucro * 0.85):
                lucros_desc += 1
                ultimo_lucro = l
        else:
            ultimo_lucro = l

    # se tem muitos lucros descrescentes na lista desc
    if lucros_desc == (ctrl - 1):
        logger.info(f"{lucros_desc} lucros decrescendo - {data_l} - {lucros}")
        return False

    # verifica se o lucro dos ultimos 12m esta muito abaixo do ultimo ano
    try:
        lucro_ultimo_ano = data_l[-1:]
        if ultimos_12m < (lucro_ultimo_ano * 0.6):
            logger.info(
                f"Descartando pois lucros de 12m com {ultimos_12m} e último ano {lucro_ultimo_ano} - {data_l}"
            )
            return False
    except Exception:
        logger.exception("Exception")
        return False

    return True


def lucro_resultado_geral(data, media):
    # se percentile for menor que zero ou media menor que zero
    p = 0
    try:
        p = percentile([x for x in data.values()], 60)
    except:
        logger.info(f"{data} - {media}")

    if p < 0:
        logger.info(f"Lucro p60 abaixo de zero {p}")
        return False
    return True


def valida_empresa(code):
    lc, media, ultimos_12m = get_lucro_details(code)

    if lc and media and ultimos_12m:
        status = valida_ultimos_lucros(lc, ultimos_12m)
        if not status:
            logger.info(f"Descartando {code} pelos últimos lucros")

        if status:
            # somente valida o geral se os ultimos forem positivos
            status = lucro_resultado_geral(lc, media)
            if not status:
                logger.info(f"Descartado {code} pelos lucros históricos negativos")
    else:
        logger.info(f"Falha nos dados para {code} - {lc} - {media} - {ultimos_12m}")
        return False

    return status


def get_lucro_details(code):
    details = db.consulta_detalhes("dre", code)

    lc = {}
    ultimos_12m = None
    for row in details[0]:
        if row["tipo"] in ["Lucro Líquido - (R$) format_quote", "Lucro Líquido - (R$)"]:
            periodo = row["periodo"]
            lucro = row["valor"]
            if periodo == "Últ. 12M":
                ultimos_12m = lucro
            else:
                lc[int(periodo)] = float(lucro)

    if not ultimos_12m and lc:
        # caso nao exista 12m usa o ultimo ano
        ultimos_12m = list(lc.values())[0]
        logger.warning(f"Sem 12m para {code}. Usando {ultimos_12m} em {lc}")

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
