import logging
import warnings
from distutils.util import strtobool

import pandas as pd
from app.application import db, financial, lucros
from app.application.utils import safe_div

warnings.filterwarnings("ignore")


logger = logging.getLogger(__name__)


def get_estrategia(estrategia):
    mp = {
        "ev_ebit_roic": (
            "EVSobreEBIT",
            "ROIC",
        ),
        "pl_roe": (
            "precoSobreLucro",
            "ROE",
        ),
    }
    return mp[estrategia]


def filter_on_sale(df):
    df = df[((df.stockPrice / df.ValorPatrimonialPorAcao) <= 1) & (df.pegr <= 1)]
    return df


def filter_per_sector(df, sector):
    df = df[df.setor == sector]
    return df


def filter_by_indicators(valor, performance, liquidez_media_minima=100000):
    data = db.consulta_detalhes("financial")

    df = pd.DataFrame(data)
    df.set_index("code")

    print(df.emRecuperacaoJudicial == True)

    df = df[
        (df.liquidezMediaDiaria > liquidez_media_minima)
        & (df.emRecuperacaoJudicial == False)
        & (df.precoSobreLucro > 0)
        & (df.margemLiquida >= 4)
        & ((df.freeFloat >= 15) | (pd.isnull(df.freeFloat)))
        # & ((df.tagAlong >= 80) | (pd.isnull(df.freeFloat)))
        & ((df.divSobreEbit <= 5) | (pd.isnull(df.divSobreEbit)))
        & ((df.pegr <= 8) | (pd.isnull(df.pegr)))
        & (getattr(df, performance) >= 0)
        & ((df.ROE >= 15) | (pd.isnull(df.ROE)))
        # & ((df.CagrLucrosCincoAnos >= -10) | (df.CagrReceitasCincoAnos >= -10))
    ]

    return df


def stocks_filter(estrategia, payload, valor, performance):
    df = filter_by_indicators(valor, performance)

    on_sale = payload.get("scopedVars").get("on_sale").get("text")
    if on_sale.lower() == "yes":
        df = filter_on_sale(df)

    sector = payload.get("scopedVars").get("sector").get("text")
    if sector.lower() != "all":
        df = filter_per_sector(df, sector)

    if estrategia == "ev_ebit_roic":
        # Essas métricas não funcionam para instituições financeiras
        df = df[(df.setor != "Financeiro e Outros")]

    # setores que Johnny não gosta
    df = df[(df.subsetor != "Construção Civil")]

    return df


def sort_magic_formula(estrategia, payload):
    valor, performance = get_estrategia(estrategia)

    df = stocks_filter(estrategia, payload, valor, performance)
    valor_ordered = df.sort_values(by=[valor])["code"].values
    performance_ordered = df.sort_values(by=[performance], ascending=False)[
        "code"
    ].values

    ranking = pd.DataFrame()
    ranking["position"] = range(1, valor_ordered.size + 1)
    ranking[valor] = valor_ordered
    ranking[performance] = performance_ordered

    valor_list = ranking.pivot_table(columns=valor, values="position")
    performance_list = ranking.pivot_table(columns=performance, values="position")
    concatenado = pd.concat([valor_list, performance_list])

    rank = concatenado.dropna(axis=1).sum()
    rank_sorted = rank.sort_values()[:70]

    return rank_sorted


def rank(estrategia, payload):
    rank_sorted = sort_magic_formula(estrategia, payload)

    logger.info(payload)

    rank_validated = []
    empresas_ranking = set()
    lucros_status = False
    num_empresas = (
        payload.get("scopedVars").get("num_empresas").get("text")
        if payload.get("scopedVars").get("num_empresas").get("text")
        else 30
    )
    valida_lucros = bool(
        strtobool(payload.get("scopedVars").get("valida_lucros").get("text"))
    )
    ranking = 0
    for code, score in rank_sorted.iteritems():
        if valida_lucros:
            logger.info(f"Analisando os lucros de {code}")
            if lucros.valida_empresa(code):
                lucros_status = True
        else:
            lucros_status = True

        if lucros_status:
            empresas_ranking.add(code[0:4])

            # adiciona indicadores
            ind = financial.financial_get_indicators(code)

            technical = db.consulta_detalhes("technical", code)[0]
            try:
                ind_1, ind_2 = int(technical["RSI(14)"][0]), technical["RSI(14)"][1]
            except Exception:
                ind_1, ind_2 = "", ""

            rank_validated.append(
                [
                    ranking,
                    code,
                    ind["segmentoListagem"],
                    ind["subsetor"],
                    ind["precoSobreLucro"],
                    ind["ROE"],
                    ind["EVSobreEBIT"],
                    ind["ROIC"],
                    ind["pegr"],
                    ind["margemLiquida"],
                    ind["divSobreEbit"],
                    ind["CagrLucrosCincoAnos"],
                    safe_div(ind["stockPrice"], ind["ValorPatrimonialPorAcao"]),
                    ind["stockPrice"],
                    ind["valorIntriseco"],
                    ind["dividendos"],
                    f"{ind_1} ({ind_2})",
                ]
            )
            ranking += 1

        if len(empresas_ranking) == int(num_empresas):
            break

    logger.info(
        "Gerado o ranking com {} empresas de um total de {} tickers".format(
            len(empresas_ranking), len(rank_sorted)
        )
    )

    return rank_validated


def columns():
    return [
        {"text": "SC.", "type": "number"},
        {"text": "CODE", "type": "string"},
        {"text": "SEGMENTO", "type": "string"},
        {"text": "SECTOR", "type": "string"},
        {"text": "P/L", "type": "number"},
        {"text": "ROE", "type": "number"},
        {"text": "EV/EBIT", "type": "number"},
        {"text": "ROIC", "type": "number"},
        {"text": "PEGR", "type": "number"},
        {"text": "MARG", "type": "number"},
        {"text": "DL/EBIT", "type": "number"},
        {"text": "CAGR LL", "type": "number"},
        {"text": "P/VPA", "type": "number"},
        {"text": "PREÇO", "type": "number"},
        {"text": "INTR.", "type": "number"},
        {"text": "DY", "type": "number"},
        {"text": "RSI", "type": "number"},
    ]
