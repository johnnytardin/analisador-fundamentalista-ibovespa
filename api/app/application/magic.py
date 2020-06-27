import logging

from app.application import db
from app.application import lucros
from app.application import financial

import pandas as pd
import warnings

warnings.filterwarnings("ignore")


logger = logging.getLogger(__name__)


def get_estrategia(estrategia):
    mp = {
        "ev_ebit_roic": ("EVSobreEBIT", "ROIC",),
        "pl_roe": ("precoSobreLucro", "ROE",),
    }
    return mp[estrategia]


def filter_barganhas(df):
    df = df[(df.PSR <= 1) & (df.pegr <= 1)]
    return df


def stocks_filter(estrategia, valor, promocao=True, liquidez_media_minima=100000):
    data = db.consulta_detalhes("financial")

    df = pd.DataFrame(data)
    df.set_index("code")

    df = df[
        (df.liquidezMediaDiaria > liquidez_media_minima)
        & (df.precoSobreLucro > 0)
        & (df.freeFloat >= 15)
        & (df.margemLiquida >= 7)
        & ((df.divSobreEbit <= 5) | (pd.isnull(df.divSobreEbit)))
        & ((df.PSR <= 5) | (pd.isnull(df.PSR)))
        & ((df.pegr <= 5) | (pd.isnull(df.pegr)))
        & (getattr(df, valor) > 0)
    ]

    if promocao:
        df = filter_barganhas(df)

    # Essas métricas não funcionam para instituições financeiras
    if estrategia == "ev_ebit_roic":
        df = df[(df.setor != "Financeiro e Outros")]

    return df


def rank(estrategia, promocao):
    valor, performance = get_estrategia(estrategia)

    df = stocks_filter(estrategia, valor, promocao)
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
    rank_sorted = rank.sort_values()[:50]

    rank_validated = []
    for code, score in rank_sorted.iteritems():
        if lucros.valida_empresa(code):
            # adiciona indicadores
            ind = financial.financial_get_indicators(code)

            rank_validated.append(
                [
                    score,
                    code,
                    ind["precoSobreLucro"],
                    ind["pegr"],
                    ind["PSR"],
                    ind["ROE"],
                    ind["margemLiquida"],
                    ind["divSobreEbit"],
                    ind["CagrLucrosCincoAnos"],
                    ind["ValorPatrimonialPorAcao"],
                    ind["stockPrice"],
                    ind["dividendos"],
                ]
            )

    return rank_validated


def columns():
    return [
        {"text": "SCORE", "type": "number"},
        {"text": "CODE", "type": "string"},
        {"text": "P/L", "type": "number"},
        {"text": "PEGR", "type": "number"},
        {"text": "PSR", "type": "number"},
        {"text": "ROE", "type": "number"},
        {"text": "MARGEM", "type": "number"},
        {"text": "DL/EBIT", "type": "number"},
        {"text": "CAGR LL", "type": "number"},
        {"text": "VPA", "type": "number"},
        {"text": "PREÇO", "type": "number"},
        {"text": "DY", "type": "number"},
    ]
