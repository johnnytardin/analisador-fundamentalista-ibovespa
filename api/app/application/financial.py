import logging
import json

import app.application.db as db


logger = logging.getLogger(__name__)


def financial_all_stocks():
    f = db.consulta_detalhes("financial", None)

    details = []
    for row in f:
        details.append(
            [
                row["code"],
                row["setor"],
                row["subsetor"],
                row["segmento"],
                row["precoSobreVP"],
                row["precoSobreLucro"],
                row["precoSobreEBITDA"],
                row["precoSobreEBIT"],
                row["precoSobreAtivo"],
                row["EVSobreEBITDA"],
                row["EVSobreEBIT"],
                row["PSR"],
                row["precoSobreCapitalGiro"],
                row["precoSobreAtivoCirculante"],
                row["margemBruta"],
                row["margemEBITDA"],
                row["margemEBIT"],
                row["margemLiquida"],
                row["giroAtivos"],
                row["ROE"],
                row["ROA"],
                row["ROIC"],
                row["lucroPorAcao"],
                row["ValorPatrimonialPorAcao"],
                row["divSobrePatrimonio"],
                row["divSobreEbitda"],
                row["divSobreEbit"],
                row["PatrimonioSobreAtivos"],
                row["PassivosSobreAtivos"],
                row["liquidezCorrente"],
                row["CagrReceitasCincoAnos"],
                row["CagrLucrosCincoAnos"],
                row["liquidezMediaDiaria"],
                row["patrimonioLiquido"],
                row["dividendos"],
                row["stockPrice"],
                row["valorMercado"],
                row["max52sem"],
                row["min52sem"],
                row["Valorizacao12M"],
                row["ValorizacaoMesAtual"],
                row["lucroLiquido"],
                row["freeFloat"],
                row["tagAlong"],
                row["valorIntriseco"],
                row["percentualDesconto"],
                row["PercDistanciaMin52sem"],
                row["score"],
            ]
        )
    return details


def financial(stock):
    f = db.consulta_detalhes("financial", stock)[0]

    details = []
    for k, v in f.items():
        details.append([k, v])
    return details


def columns():
    return [
        {"text": "code", "type": "number"},
        {"text": "precoSobreVP", "type": "number"},
        {"text": "precoSobreLucro", "type": "number"},
        {"text": "precoSobreEBITDA", "type": "number"},
        {"text": "precoSobreEBIT", "type": "number"},
        {"text": "precoSobreAtivo", "type": "number"},
        {"text": "EVSobreEBITDA", "type": "number"},
        {"text": "EVSobreEBIT", "type": "number"},
        {"text": "PSR", "type": "number"},
        {"text": "precoSobreCapitalGiro", "type": "number"},
        {"text": "precoSobreAtivoCirculante", "type": "number"},
        {"text": "margemBruta", "type": "number"},
        {"text": "margemEBITDA", "type": "number"},
        {"text": "margemEBIT", "type": "number"},
        {"text": "margemLiquida", "type": "number"},
        {"text": "giroAtivos", "type": "number"},
        {"text": "ROE", "type": "number"},
        {"text": "ROA", "type": "number"},
        {"text": "ROIC", "type": "number"},
        {"text": "lucroPorAcao", "type": "number"},
        {"text": "ValorPatrimonialPorAcao", "type": "number"},
        {"text": "divSobrePatrimonio", "type": "number"},
        {"text": "divSobreEbitda", "type": "number"},
        {"text": "divSobreEbit", "type": "number"},
        {"text": "PatrimonioSobreAtivos", "type": "number"},
        {"text": "PassivosSobreAtivos", "type": "number"},
        {"text": "liquidezCorrente", "type": "number"},
        {"text": "CagrReceitasCincoAnos", "type": "number"},
        {"text": "CagrLucrosCincoAnos", "type": "number"},
        {"text": "liquidezMediaDiaria", "type": "number"},
        {"text": "patrimonioLiquido", "type": "number"},
        {"text": "dividendos", "type": "number"},
        {"text": "stockPrice", "type": "number"},
        {"text": "setor", "type": "number"},
        {"text": "subsetor", "type": "number"},
        {"text": "segmento", "type": "number"},
        {"text": "valorMercado", "type": "number"},
        {"text": "max52sem", "type": "number"},
        {"text": "min52sem", "type": "number"},
        {"text": "Valorizacao12M", "type": "number"},
        {"text": "ValorizacaoMesAtual", "type": "number"},
        {"text": "lucroLiquido", "type": "number"},
        {"text": "freeFloat", "type": "number"},
        {"text": "tagAlong", "type": "number"},
        {"text": "valorIntriseco", "type": "number"},
        {"text": "percentualDesconto", "type": "number"},
        {"text": "PercDistanciaMin52sem", "type": "number"},
        {"text": "score", "type": "number"},
    ]


def columns_all():
    return [
        {"text": "tipo", "type": "string"},
        {"text": "valor", "type": "number"},
    ]
