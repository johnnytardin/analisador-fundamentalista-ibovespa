#!/usr/bin/env python3
import datetime
from uuid import uuid4

import graham
import status
import stocks
import db


def normaliza_valor(data, replace=None):
    data = str(data)
    fm = (
        data.replace("\n", "")
        .replace("%", "")
        .replace(".", "")
        .replace(",", ".")
        .replace("R$", "")
        .replace(" ", "")
    )
    try:
        n = float(fm)
    except ValueError:
        if fm == "-":
            return replace
        return None
    return n


def details(code, coleta_id):
    financial = {}

    # Get more information
    print(f"Getting more information from stock {code}")
    status_data = status.get_specific_data(code)

    liqCorr = normaliza_valor(status_data["LIQUIDEZ CORRENTE"])
    roe = normaliza_valor(status_data["ROE"])
    roic = normaliza_valor(status_data["ROIC"])
    pvp = normaliza_valor(status_data["P/VP"])
    pl = normaliza_valor(status_data["P/L"])
    dy = normaliza_valor(status_data["DIVIDEND YIELD"], 0)
    divPat = normaliza_valor(status_data["DÍVIDA LÍQUIDA / PATRIMÔNIO"])

    financial["code"] = code
    financial["precoSobreVP"] = pvp
    financial["precoSobreLucro"] = pl
    financial["precoSobreEBITDA"] = normaliza_valor(status_data["P/EBITDA"])
    financial["precoSobreEBIT"] = normaliza_valor(status_data["P/EBIT"])
    financial["precoSobreAtivo"] = normaliza_valor(status_data["P/ATIVO"])
    financial["EVSobreEBITDA"] = normaliza_valor(status_data["EV/EBITDA"])
    financial["EVSobreEBIT"] = normaliza_valor(status_data["EV/EBIT"])
    financial["PSR"] = normaliza_valor(status_data["PSR"])
    financial["precoSobreCapitalGiro"] = normaliza_valor(status_data["P/CAP.GIRO"])
    financial["precoSobreAtivoCirculante"] = normaliza_valor(
        status_data["P/ATIVO CIRC LIQ"]
    )
    financial["margemBruta"] = normaliza_valor(status_data["MARGEM BRUTA"])
    financial["margemEBITDA"] = normaliza_valor(status_data["MARGEM EBITDA"])
    financial["margemEBIT"] = normaliza_valor(status_data["MARGEM EBIT"])
    financial["margemLiquida"] = normaliza_valor(status_data["MARGEM LÍQUIDA"])
    financial["giroAtivos"] = normaliza_valor(status_data["GIRO ATIVOS"])
    financial["ROE"] = roe
    financial["ROA"] = normaliza_valor(status_data["ROA"])
    financial["ROIC"] = roic
    financial["lucroPorAcao"] = normaliza_valor(status_data["LPA"])
    financial["ValorPatrimonialPorAcao"] = normaliza_valor(status_data["VPA"])
    financial["divSobrePatrimonio"] = divPat
    financial["divSobreEbitda"] = normaliza_valor(
        status_data["DÍVIDA LÍQUIDA / EBITDA"]
    )
    financial["divSobreEbit"] = normaliza_valor(status_data["DÍVIDA LÍQUIDA / EBIT"])
    financial["PatrimonioSobreAtivos"] = normaliza_valor(
        status_data["PATRIMÔNIO / ATIVOS"]
    )
    financial["PassivosSobreAtivos"] = normaliza_valor(status_data["PASSIVOS / ATIVOS"])
    financial["liquidezCorrente"] = liqCorr
    financial["CagrReceitasCincoAnos"] = normaliza_valor(
        status_data["CAGR RECEITAS 5 ANOS"]
    )
    financial["CagrLucrosCincoAnos"] = normaliza_valor(
        status_data["CAGR LUCROS 5 ANOS"]
    )
    financial["liquidezMediaDiaria"] = normaliza_valor(
        status_data["LIQUIDEZ MÉDIA DIÁRIA"]
    )
    financial["dividendos"] = dy
    financial["stockPrice"] = normaliza_valor(status_data["VALOR ATUAL"])
    financial["setor"] = status_data["SETOR DE ATUAÇÂO"]
    financial["subsetor"] = status_data["SUBSETOR DE ATUAÇÂO"]
    financial["segmento"] = status_data["SEGMENTO DE ATUAÇÂO"]
    financial["valorMercado"] = normaliza_valor(status_data["VALOR DE MERCADO"])
    financial["max52sem"] = normaliza_valor(status_data["MÁX. 52 SEMANAS"])
    financial["min52sem"] = normaliza_valor(status_data["MIN. 52 SEMANAS"])
    financial["Valorizacao12M"] = normaliza_valor(status_data["VALORIZAÇÃO (12M)"])
    financial["ValorizacaoMesAtual"] = normaliza_valor(
        status_data["VALORIZAÇÃO (MÊS ATUAL)"]
    )
    financial["freeFloat"] = normaliza_valor(status_data["FREE FLOAT"])
    financial["tagAlong"] = normaliza_valor(status_data["TAG ALONG"])
    financial["segmentoListagem"] = normaliza_valor(status_data["SEGMENTO DE LISTAGEM"])

    # intriseco
    financial["valorIntriseco"] = graham.valor_intriseco(
        financial["lucroPorAcao"], financial["ValorPatrimonialPorAcao"]
    )

    # PEG Ratio
    try:
        pegr = financial["precoSobreLucro"] / financial["CagrLucrosCincoAnos"]
    except (ZeroDivisionError, TypeError):
        pegr = None
    financial["pegr"] = pegr

    # percentual de desconto
    try:
        p_desc = ((financial["stockPrice"] / financial["valorIntriseco"]) - 1) * 100
    except ZeroDivisionError:
        p_desc = 0
    financial["percentualDesconto"] = p_desc

    # distancia para a cotação mínima (server para tentar pegar um bom time)
    distancia = None
    if financial["max52sem"] and financial["min52sem"]:
        diff_min_max = financial["max52sem"] - financial["min52sem"]
        diff_atual = financial["stockPrice"] - financial["min52sem"]
        try:
            distancia = (diff_atual / diff_min_max) * 100
        except ZeroDivisionError:
            distancia = 0
    financial["PercDistanciaMin52sem"] = distancia

    # outros dados
    dre = status_data["dre"]

    return (financial, dre)


def main():
    st = stocks.get_stocks_tickers()

    coleta_id = str(uuid4())
    timestamp = datetime.datetime.now().isoformat()

    for stock in st:
        try:
            financial, dre = details(stock, coleta_id)
        except Exception as err:
            print("Falha coletando os dados do papel {}. Causa: {}".format(stock, err))
        else:
            db.insert_data("financial", stock, coleta_id, timestamp, financial)
            db.insert_data("dre", stock, coleta_id, timestamp, dre)


if __name__ == "__main__":
    main()
