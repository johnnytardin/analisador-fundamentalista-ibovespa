import logging

import app.application.db as db
import app.application.lucros as lucros

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


def stocks_list(estrategia, valor, liquidez_media_minima=1000000):
    data = db.consulta_detalhes("financial")

    df = pd.DataFrame(data)
    df.set_index("code")
    df = df[
        (df.liquidezMediaDiaria > liquidez_media_minima)
        & (df.liquidezCorrente > 0.75)
        & (df.precoSobreLucro > 0)
        & (df.freeFloat > 15)
        & (df.margemLiquida >= 7)
        & (df[valor] > 0)
    ]

    # Essas métricas não funcionam para instituições financeiras
    if estrategia == "ev_ebit_roic":
        df = df[(df.setor != "Financeiro e Outros")]

    return df


def rank(estrategia):
    valor, performance = get_estrategia(estrategia)

    df = stocks_list(estrategia, valor)
    valor_ordered = df.sort_values(by=[valor])["code"][:150].values
    performance_ordered = df.sort_values(by=[performance], ascending=False)["code"][
        :150
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
            rank_validated.append([score, code])

    return rank_validated


def columns():
    return [
        {"text": "score", "type": "number"},
        {"text": "code", "type": "string"},
    ]
