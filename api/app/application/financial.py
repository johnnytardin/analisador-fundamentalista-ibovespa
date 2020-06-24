import logging
import json

import app.application.db as db


logger = logging.getLogger(__name__)


def financial_global(stock):
    # TODO: desenvolver uma forma de retornar todos os daos para filtro no grafana
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
        {"text": "tipo", "type": "string"},
        {"text": "valor", "type": "number"},
    ]
