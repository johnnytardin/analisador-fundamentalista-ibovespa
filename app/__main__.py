#!/usr/bin/env python3
import datetime
from uuid import uuid4

from tabulate import tabulate

import graham
import fundamentus
import status
import db
from waitingbar import WaitingBar


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


def lista_papeis():
    lista = fundamentus.get_data()

    # Transform em uma lista, agora preciso passar para formato JSON
    array_format = list(lista.items())

    hashes_list = []
    # First include the list of all hashes
    for i in range(0, len(array_format)):
        hashes_list.append(array_format[i][1])

    stocks = []
    # Then from a list of hashes we will transform to a list of stocks
    for i in range(0, len(hashes_list)):
        for key in hashes_list[i]:
            # Adds stockCode
            hashes_list[i][key]["stockCode"] = key
            stocks.append(hashes_list[i][key])
    return stocks


def details(stock, coleta_id):
    newStock = {}
    newStock["coletaUUID"] = coleta_id
    newStock["timestamp"] = datetime.datetime.now()
    newStock["stockCode"] = stock["stockCode"]

    # Get more information
    print("Getting more information from stock ", newStock["stockCode"])
    status_data = status.get_specific_data(newStock["stockCode"])

    dre = status_data["dre"]

    liqCorr = normaliza_valor(status_data["LIQUIDEZ CORRENTE"])
    roe = normaliza_valor(status_data["ROE"])
    roic = normaliza_valor(status_data["ROIC"])
    pvp = normaliza_valor(status_data["P/VP"])
    pl = normaliza_valor(status_data["P/L"])
    dy = normaliza_valor(status_data["DIVIDEND YIELD"], 0)
    patrLiq = normaliza_valor(status_data["PATRIMÔNIO LÍQUIDO"])
    divPat = normaliza_valor(status_data["DÍVIDA LÍQUIDA / PATRIMÔNIO"])
    newStock["precoSobreVP"] = pvp
    newStock["precoSobreLucro"] = pl
    newStock["precoSobreEBITDA"] = normaliza_valor(status_data["P/EBITDA"])
    newStock["precoSobreEBIT"] = normaliza_valor(status_data["P/EBIT"])
    newStock["precoSobreAtivo"] = normaliza_valor(status_data["P/ATIVO"])
    newStock["EVSobreEBITDA"] = normaliza_valor(status_data["EV/EBITDA"])
    newStock["EVSobreEBIT"] = normaliza_valor(status_data["EV/EBIT"])
    newStock["PSR"] = normaliza_valor(status_data["PSR"])
    newStock["precoSobreCapitalGiro"] = normaliza_valor(status_data["P/CAP.GIRO"])
    newStock["precoSobreAtivoCirculante"] = normaliza_valor(
        status_data["P/ATIVO CIRC LIQ"]
    )
    newStock["margemBruta"] = normaliza_valor(status_data["MARGEM BRUTA"])
    newStock["margemEBITDA"] = normaliza_valor(status_data["MARGEM EBITDA"])
    newStock["margemEBIT"] = normaliza_valor(status_data["MARGEM EBIT"])
    newStock["margemLiquida"] = normaliza_valor(status_data["MARGEM LÍQUIDA"])
    newStock["giroAtivos"] = normaliza_valor(status_data["GIRO ATIVOS"])
    newStock["ROE"] = roe
    newStock["ROA"] = normaliza_valor(status_data["ROA"])
    newStock["ROIC"] = roic
    newStock["lucroPorAcao"] = normaliza_valor(status_data["LPA"])
    newStock["ValorPatrimonialPorAcao"] = normaliza_valor(status_data["VPA"])
    newStock["divSobrePatrimonio"] = divPat
    newStock["divSobreEbitda"] = normaliza_valor(status_data["DÍVIDA LÍQUIDA / EBITDA"])
    newStock["divSobreEbit"] = normaliza_valor(status_data["DÍVIDA LÍQUIDA / EBIT"])
    newStock["PatrimonioSobreAtivos"] = normaliza_valor(
        status_data["PATRIMÔNIO / ATIVOS"]
    )
    newStock["PassivosSobreAtivos"] = normaliza_valor(status_data["PASSIVOS / ATIVOS"])
    newStock["liquidezCorrente"] = liqCorr
    newStock["CagrReceitasCincoAnos"] = normaliza_valor(
        status_data["CAGR RECEITAS 5 ANOS"]
    )
    newStock["CagrLucrosCincoAnos"] = normaliza_valor(status_data["CAGR LUCROS 5 ANOS"])
    newStock["liquidezMediaDiaria"] = normaliza_valor(
        status_data["LIQUIDEZ MÉDIA DIÁRIA"]
    )
    newStock["patrimonioLiquido"] = patrLiq
    newStock["dividendos"] = dy
    newStock["stockPrice"] = normaliza_valor(status_data["VALOR ATUAL"])
    newStock["setor"] = status_data["SETOR DE ATUAÇÂO"]
    newStock["subsetor"] = status_data["SUBSETOR DE ATUAÇÂO"]
    newStock["segmento"] = status_data["SEGMENTO DE ATUAÇÂO"]
    newStock["max52sem"] = normaliza_valor(status_data["MÁX. 52 SEMANAS"])
    newStock["min52sem"] = normaliza_valor(status_data["MIN. 52 SEMANAS"])
    newStock["Valorizacao12M"] = normaliza_valor(status_data["VALORIZAÇÃO (12M)"])
    newStock["ValorizacaoMesAtual"] = normaliza_valor(
        status_data["VALORIZAÇÃO (MÊS ATUAL)"]
    )
    newStock["lucroLiquido"] = normaliza_valor(status_data["LUCRO LIQUIDO 12M"])

    # intriseco
    newStock["valorIntriseco"] = graham.valor_intriseco(
        newStock["lucroPorAcao"], newStock["ValorPatrimonialPorAcao"]
    )

    # percentual de desconto
    try:
        p_desc = ((newStock["stockPrice"] / newStock["valorIntriseco"]) - 1) * 100
    except ZeroDivisionError:
        p_desc = 0
    newStock["percentualDesconto"] = p_desc

    # distancia para a cotação mínima (server para tentar pegar um bom time)
    distancia = None
    if newStock["max52sem"] and newStock["min52sem"]:
        diff_min_max = newStock["max52sem"] - newStock["min52sem"]
        diff_atual = newStock["stockPrice"] - newStock["min52sem"]
        try:
            distancia = (diff_atual / diff_min_max) * 100
        except ZeroDivisionError:
            distancia = 0
    newStock["PercDistanciaMin52sem"] = distancia

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

    if newStock["CagrLucrosCincoAnos"]:
        score_steps += 1
        if newStock["CagrLucrosCincoAnos"] > 1:
            nota += 1

    if newStock["CagrReceitasCincoAnos"]:
        score_steps += 1
        if newStock["CagrReceitasCincoAnos"] > 1:
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

    if newStock["margemLiquida"]:
        score_steps += 1
        if newStock["margemLiquida"] >= 20:
            nota += 1
        elif newStock["margemLiquida"] >= 10:
            nota += 0.5

    score_steps += 1
    if p_desc < -10:
        nota += 1

    newStock["score"] = float(nota) / score_steps * 10.0

    return newStock, dre


def save_on_db(tipo, data):
    if tipo == "fundamentus":
        db.insert(data)
    elif tipo == "dre":
        db.insert_dre(data)


def main():
    THE_BAR = WaitingBar("[*] Downloading...")
    stocks = lista_papeis()
    THE_BAR.stop()

    coleta_id = str(uuid4())

    final_stocks = []
    for stock in stocks:
        d = []
        try:
            d, dre = details(stock, coleta_id)
            final_stocks.append(d)
        except Exception as err:
            print(
                "Falha coletando os dados do papel {}. Causa: {}".format(
                    stock["stockCode"], err
                )
            )
        else:
            save_on_db("fundamentus", [d])
            save_on_db("dre", dre)


if __name__ == "__main__":
    main()
