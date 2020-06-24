#!/usr/bin/env python3
import datetime
from uuid import uuid4

import graham
import status
import stocks
import technical
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
    patrLiq = normaliza_valor(status_data["PATRIMÔNIO LÍQUIDO"])
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
    financial["divSobreEbitda"] = normaliza_valor(status_data["DÍVIDA LÍQUIDA / EBITDA"])
    financial["divSobreEbit"] = normaliza_valor(status_data["DÍVIDA LÍQUIDA / EBIT"])
    financial["PatrimonioSobreAtivos"] = normaliza_valor(
        status_data["PATRIMÔNIO / ATIVOS"]
    )
    financial["PassivosSobreAtivos"] = normaliza_valor(status_data["PASSIVOS / ATIVOS"])
    financial["liquidezCorrente"] = liqCorr
    financial["CagrReceitasCincoAnos"] = normaliza_valor(
        status_data["CAGR RECEITAS 5 ANOS"]
    )
    financial["CagrLucrosCincoAnos"] = normaliza_valor(status_data["CAGR LUCROS 5 ANOS"])
    financial["liquidezMediaDiaria"] = normaliza_valor(
        status_data["LIQUIDEZ MÉDIA DIÁRIA"]
    )
    financial["patrimonioLiquido"] = patrLiq
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
    financial["lucroLiquido"] = normaliza_valor(status_data["LUCRO LIQUIDO 12M"])
    financial["freeFloat"] = normaliza_valor(status_data["FREE FLOAT"])
    financial["tagAlong"] = normaliza_valor(status_data["TAG ALONG"])

    # intriseco
    financial["valorIntriseco"] = graham.valor_intriseco(
        financial["lucroPorAcao"], financial["ValorPatrimonialPorAcao"]
    )

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

    # score
    nota = 0
    score_steps = 0

    score_steps += 1
    if patrLiq > 2000000000:
        nota += 1

    if liqCorr:
        score_steps += 1
        if liqCorr > 1.5:
            nota += 1

    if roe:
        score_steps += 1
        if roe > 20:
            nota += 1
        elif roe >= 10:
            nota += 0.5

    if roic:
        score_steps += 1
        if roic > 20:
            nota += 1
        elif roic >= 10:
            nota += 0.5

    if divPat:
        score_steps += 1
        if divPat < 0.5 and divPat >= 0:
            """
            Resultados inferiores a uma unidade indicam que a empresa deve menos
            do que ela vale. Se o indicativo apontar vários múltiplos, significa que a
            empresa opera seriamente endividada e merece ser evitada.
            """
            nota += 1

    if financial["CagrLucrosCincoAnos"]:
        score_steps += 1
        if financial["CagrLucrosCincoAnos"] > 1:
            nota += 1

    if financial["CagrReceitasCincoAnos"]:
        score_steps += 1
        if financial["CagrReceitasCincoAnos"] > 1:
            nota += 1

    if pvp:
        score_steps += 1
        if pvp < 2 and pvp > 0:
            nota += 1

    if pl:
        score_steps += 1
        if pl <= 20 and pl > 0:
            nota += 1

    score_steps += 1
    if dy > 2.5:
        nota += 1

    if financial["margemLiquida"]:
        score_steps += 1
        if financial["margemLiquida"] >= 20:
            nota += 1
        elif financial["margemLiquida"] >= 10:
            nota += 0.5

    score_steps += 1
    if p_desc < -10:
        nota += 1

    financial["score"] = float(nota) / score_steps * 10.0

    # outros dados
    dre = status_data["dre"]
    indicators = technical.get_indicators(code)
    averages = technical.get_moving_averages(code)

    return (financial, dre, indicators, averages)


def main():
    st = stocks.stocks_codes()

    coleta_id = str(uuid4())
    timestamp = datetime.datetime.now().isoformat()

    for stock in st:
        try:
            financial, dre, indicators, averages = details(stock, coleta_id)
        except Exception as err:
            print("Falha coletando os dados do papel {}. Causa: {}".format(stock, err))
        else:
            db.insert_data("financial", stock, coleta_id, timestamp, financial)
            db.insert_data("dre", stock, coleta_id, timestamp, dre)
            db.insert_data("indicators", stock, coleta_id, timestamp, indicators)
            db.insert_data("averages", stock, coleta_id, timestamp, averages)


if __name__ == "__main__":
    main()
