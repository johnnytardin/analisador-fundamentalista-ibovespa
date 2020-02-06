#!/usr/bin/env python3
import datetime
from uuid import uuid4

from tabulate import tabulate

import graham
import fundamentus
import db
from waitingbar import WaitingBar


def normaliza_valor(data):
    try:
        n = float(
            data.replace("\n", "").replace("%", "").replace(".", "").replace(",", ".")
        )
    except ValueError:
        return None
    return n


if __name__ == "__main__":
    coleta_id = str(uuid4())

    THE_BAR = WaitingBar("[*] Downloading...")

    lista = fundamentus.get_data()
    THE_BAR.stop()
    # print("Get all stocks data")

    # Transform em uma lista, agora preciso passar para formato JSON
    array_format = list(lista.items())

    # print(array_format, len(array_format))

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

    #     json_format = {
    #     "0": {
    #         "DAGB33": {
    #             "Cresc.5a": "46,43%",
    #             "DY": "0,00%",
    #             "Div.Brut/Pat.": "1,37",
    #             "EV/EBITDA": "4,75%",
    #             "EV/EBIT": "0,00",
    #             "Liq.2m.": "916.730,00",
    #             "Liq.Corr.": "1,16",
    #             "Mrg.Liq.": "0,38%",
    #             "Mrg.Ebit.": "0,38%",
    #             "P/Ativ.Circ.Liq.": "0,00",
    #             "P/Ativo": "0,000",
    #             "P/Cap.Giro": "0,00",
    #             "P/EBIT": "0,00",
    #             "P/L": "0,00",
    #             "P/VP": "0,00",
    #             "PSR": "0,000",
    #             "Pat.Liq": "9.803.230.000,00",
    #             "ROE": "-0,47%",
    #             "ROIC": "4,59%",
    #             "cotacao": "480,00",
    #             "nota": 0.5
    #         }
    #     }
    # }

    # Calculate the score of the stock
    final_stocks = []
    for stock in stocks:
        newStock = {}
        newStock["coletaUUID"] = coleta_id
        newStock["timestamp"] = datetime.datetime.now()
        newStock["liquidezDoisMeses"] = normaliza_valor(stock["Liq.2m."])

        newStock["stockCode"] = stock["stockCode"]

        # Get more information
        print("Getting more information from stock ", newStock["stockCode"])
        specific_data = fundamentus.get_specific_data(newStock["stockCode"])

        # Add everything to the object
        patrLiq = normaliza_valor(specific_data["Patrim. Líq"])
        liqCorr = normaliza_valor(specific_data["Liquidez Corr"])
        roe = normaliza_valor(specific_data["ROE"])
        roic = normaliza_valor(specific_data["ROIC"])
        cresc = normaliza_valor(specific_data["Cres. Rec (5a)"])
        pvp = normaliza_valor(specific_data["P/VP"])
        pl = normaliza_valor(specific_data["P/L"])
        dy = normaliza_valor(specific_data["Div. Yield"])

        divPat = normaliza_valor(specific_data["Div Br/ Patrim"])
        divPat = divPat if divPat else 0

        newStock["patrimonioLiquido"] = patrLiq
        newStock["liquidezCorrente"] = liqCorr
        newStock["ROE"] = roe
        newStock["divSobrePatrimonio"] = divPat
        newStock["crescimentoCincoAnos"] = cresc
        newStock["precoSobreVP"] = pvp
        newStock["precoSobreLucro"] = pl
        newStock["dividendos"] = dy
        newStock["stockPrice"] = normaliza_valor(specific_data["Cotação"])
        newStock["PSR"] = normaliza_valor(specific_data["PSR"])
        newStock["precoSobreAtivo"] = normaliza_valor(specific_data["P/Ativos"])
        newStock["precoSobreCapitalGiro"] = normaliza_valor(
            specific_data["P/Cap. Giro"]
        )
        newStock["precoSobreEBIT"] = normaliza_valor(specific_data["P/EBIT"])
        newStock["precoSobreAtivoCirculante"] = normaliza_valor(
            specific_data["P/Ativ Circ Liq"]
        )
        newStock["EVSobreEBIT"] = normaliza_valor(specific_data["EV / EBIT"])

        newStock["EVSobreEBITDA"] = normaliza_valor(specific_data["EV / EBITDA"])
        newStock["margemEBIT"] = normaliza_valor(specific_data["Marg. EBIT"])
        newStock["margemLiquida"] = normaliza_valor(specific_data["Marg. Líquida"])
        newStock["ROIC"] = normaliza_valor(specific_data["ROIC"])

        newStock["tipo"] = specific_data["Tipo"]
        newStock["name"] = specific_data["Empresa"]
        newStock["setor"] = specific_data["Setor"]
        newStock["subsetor"] = specific_data["Subsetor"]
        newStock["max52sem"] = normaliza_valor(specific_data["Max 52 sem"])
        newStock["min52sem"] = normaliza_valor(specific_data["Min 52 sem"])
        newStock["volMed2M"] = normaliza_valor(specific_data["Vol $ méd (2m)"])
        newStock["valorMercado"] = normaliza_valor(specific_data["Valor de mercado"])
        newStock["valorFirma"] = normaliza_valor(specific_data["Valor da firma"])
        newStock["nAcoes"] = normaliza_valor(specific_data["Nro. Ações"])
        newStock["lucroPorAcao"] = normaliza_valor(specific_data["LPA"])
        newStock["ValorPatrimonialPorAcao"] = normaliza_valor(specific_data["VPA"])
        newStock["margemBruta"] = normaliza_valor(specific_data["Marg. Bruta"])
        newStock["EBITsobreAtivo"] = normaliza_valor(specific_data["EBIT / Ativo"])
        newStock["giroAtivos"] = normaliza_valor(specific_data["Giro Ativos"])
        newStock["ativo"] = normaliza_valor(specific_data["Ativo"])

        if "Lucro Líquido" in specific_data:
            newStock["lucroLiquido"] = normaliza_valor(specific_data["Lucro Líquido"])
        else:
            newStock["lucroLiquido"] = None

        if "Receita Líquida" in specific_data:
            newStock["receitaLiquida"] = normaliza_valor(
                specific_data["Receita Líquida"]
            )
        else:
            newStock["receitaLiquida"] = None

        if "Disponibilidades" in specific_data:
            newStock["disponibilidades"] = normaliza_valor(
                specific_data["Disponibilidades"]
            )
        else:
            newStock["disponibilidades"] = None

        if "Dív. Bruta" in specific_data:
            newStock["divBruta"] = normaliza_valor(specific_data["Dív. Bruta"])
        else:
            newStock["divBruta"] = None

        if "Dív. Líquida" in specific_data:
            newStock["divLiquida"] = normaliza_valor(specific_data["Dív. Líquida"])
        else:
            newStock["divLiquida"] = None

        try:
            newStock["DividaSobreAtivo"] = newStock["divBruta"] / newStock["ativo"]
        except ZeroDivisionError:
            newStock["DividaSobreAtivo"] = 0
        except TypeError:
            newStock["DividaSobreAtivo"] = None

        # intriseco
        newStock["valorIntriseco"] = graham.valor_intriseco(
            newStock["lucroPorAcao"], newStock["ValorPatrimonialPorAcao"]
        )

        # desconto
        newStock["desconto"] = (
            newStock["valorIntriseco"] - newStock["stockPrice"]
            if newStock["valorIntriseco"] > 0
            else 0
        )

        # percentual de desconto
        try:
            p_desc = ((newStock["stockPrice"] / newStock["valorIntriseco"]) - 1) * 100
        except ZeroDivisionError:
            p_desc = 0
        newStock["percentualDesconto"] = p_desc

        # distancia para a cotação mínima (server para tentar pegar um bom time)
        try:
            diff_min_max = newStock["max52sem"] - newStock["min52sem"]
        except ZeroDivisionError:
            diff_min_max = 0
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

        if cresc:
            score_steps += 1
            if cresc > 5:
                nota += 1

        score_steps += 1
        if pvp < 2 and pvp > 0:
            nota += 1

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

        # empresas com divida baixa
        if newStock["DividaSobreAtivo"]:
            score_steps += 1
            if newStock["DividaSobreAtivo"] >= 1.5 or newStock["DividaSobreAtivo"] == 0:
                # a segunda opção é para caso a empresa não tenha dívida
                nota += 1

        newStock["score"] = float(nota) / score_steps * 10.0

        final_stocks.append(newStock)

    # insere db
    db.insert(final_stocks)
