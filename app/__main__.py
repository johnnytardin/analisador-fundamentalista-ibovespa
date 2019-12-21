#!/usr/bin/env python3
import datetime
from uuid import uuid4

import graham
import fundamentus
import db



if __name__ == '__main__':
    coleta_id = str(uuid4())

    from waitingbar import WaitingBar
    
    THE_BAR = WaitingBar('[*] Downloading...')

    lista = fundamentus.get_data()
    THE_BAR.stop()
    # print("Get all stocks data")


    #Transform em uma lista, agora preciso passar para formato JSON
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
        patrLiq = float(stock["Pat.Liq"].replace('.', '').replace(',', '.'))
        liqCorr = float(stock["Liq.Corr."].replace('.', '').replace(',', '.'))
        roe = float(stock["ROE"].replace('.', '').replace(',', '.').replace('%', ''))
        divPat = float(stock["Div.Brut/Pat."].replace('.', '').replace(',', '.').replace('%', ''))
        cresc = float(stock["Cresc.5a"].replace('.', '').replace(',', '.').replace('%', ''))
        pvp = float(stock["P/VP"].replace('.', '').replace(',', '.').replace('%', ''))
        pl = float(stock["P/L"].replace('.', '').replace(',', '.').replace('%', ''))
        dy = float(stock["DY"].replace('.', '').replace(',', '.').replace('%', ''))

        newStock = {}
        newStock["coletaUUID"] = coleta_id
        newStock["stockCode"] = stock["stockCode"]
        newStock["patrimonioLiquido"] = patrLiq
        newStock["liquidezCorrente"] = liqCorr
        newStock["ROE"] = roe
        newStock["divSobrePatrimonio"] = divPat
        newStock["crescimentoCincoAnos"] = cresc
        newStock["precoSobreVP"] = pvp
        newStock["precoSobreLucro"] = pl
        newStock["dividendos"] = dy
        newStock["stockPrice"] = float(stock["cotacao"].replace('.', '').replace(',', '.'))
        newStock["PSR"] = float(stock["PSR"].replace('.', '').replace(',', '.'))
        newStock["precoSobreAtivo"] = float(stock['P/Ativo'].replace('.', '').replace(',', '.'))
        newStock["precoSobreCapitalGiro"] = float(stock['P/Cap.Giro'].replace('.', '').replace(',', '.'))
        newStock["precoSobreEBIT"] = float(stock['P/EBIT'].replace('.', '').replace(',', '.'))
        newStock["precoSobreAtivoCirculante"] = float(stock['P/Ativ.Circ.Liq.'].replace('.', '').replace(',', '.'))
        newStock["EVSobreEBIT"] = float(stock['EV/EBIT'].replace('.', '').replace(',', '.'))
        newStock["EVSobreEBITDA"] = float(stock['EV/EBITDA'].replace('.', '').replace(',', '.'))
        newStock["margemEBIT"] = float(stock["Mrg.Ebit."].replace('.', '').replace(',', '.').replace('%', ''))
        newStock["margemLiquida"] = float(stock['Mrg.Liq.'].replace('.', '').replace(',', '.').replace('%', ''))
        newStock["ROIC"] = float(stock["ROIC"].replace('.', '').replace(',', '.').replace('%', ''))
        newStock["liquidezDoisMeses"] = float(stock['Liq.2m.'].replace('.', '').replace(',', '.').replace('%', ''))
        newStock["timestamp"] = datetime.datetime.now()

        # Get more information
        print("Getting more information from stock ", newStock["stockCode"])
        specific_data = fundamentus.get_specific_data(newStock["stockCode"])

        # Add everything to the object
        newStock["tipo"] = specific_data['Tipo']
        newStock["name"] = specific_data['Empresa']
        newStock["setor"] = specific_data['Setor']
        newStock["subsetor"] = specific_data['Subsetor']
        newStock["max52sem"] = float(specific_data['Max 52 sem'].replace('.', '').replace(',', '.')) if not "-" in specific_data['Max 52 sem'] else 0
        newStock["volMed2M"] = float(specific_data['Vol $ méd (2m)'].replace('.', '').replace(',', '.')) if not "-" in specific_data['Vol $ méd (2m)'] else 0
        newStock["valorMercado"] = float(specific_data['Valor de mercado'].replace('.', '').replace(',', '.')) if not "-" in specific_data['Valor de mercado'] else 0
        newStock["valorFirma"] = float(specific_data['Valor da firma'].replace('.', '').replace(',', '.')) if not "-" in specific_data['Valor da firma'] else 0
        newStock["nAcoes"] = float(specific_data['Nro. Ações'].replace('.', '').replace(',', '.')) if not "-" in specific_data['Nro. Ações'] else 0
        newStock["lucroPorAcao"] = float(specific_data['LPA'].replace('.', '').replace(',', '.')) if not "-" in specific_data['LPA'] else 0
        newStock["ValorPatrimonialPorAcao"] = float(specific_data['VPA'].replace('.', '').replace(',', '.')) if not "-" in specific_data['VPA'] else 0
        newStock["margemBruta"] = float(specific_data['Marg. Bruta'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['Marg. Bruta'] else 0
        newStock["EBITsobreAtivo"] = float(specific_data['EBIT / Ativo'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['EBIT / Ativo'] else 0
        newStock["giroAtivos"] = float(specific_data['Giro Ativos'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['Giro Ativos'] else 0
        newStock["ativo"] = float(specific_data['Ativo'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['Ativo'] else 0

        if "Lucro Líquido" in specific_data:
            newStock["lucroLiquido"] = float(specific_data['Lucro Líquido'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['Lucro Líquido'] else 0
        else:
            newStock["lucroLiquido"] = None

        if "Receita Líquida" in specific_data:
            newStock["receitaLiquida"] = float(specific_data['Receita Líquida'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['Receita Líquida'] else 0
        else:
            newStock["receitaLiquida"] = None

        if "Disponibilidades" in specific_data:
            newStock["disponibilidades"] = float(specific_data['Disponibilidades'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['Disponibilidades'] else 0
        else:
            newStock["disponibilidades"] = None

        if "Dív. Bruta" in specific_data:
            newStock["divBruta"] = float(specific_data['Dív. Bruta'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['Dív. Bruta'] else 0
        else:
            newStock["divBruta"] = None

        if "Dív. Líquida" in specific_data:
            newStock["divLiquida"] = float(specific_data['Dív. Líquida'].replace('.', '').replace(',', '.').replace('%', '').replace("\n", "")) if not "-" in specific_data['Dív. Líquida'] else 0
        else:
            newStock["divLiquida"] = None

        # intriseco
        newStock["valorIntriseco"] = graham.valor_intriseco(newStock["lucroPorAcao"], newStock["ValorPatrimonialPorAcao"])

        # score
        nota = 0
        if patrLiq > 2000000000:
            nota += 1

        if liqCorr > 1.5:
            nota += 1

        if roe > 20:
            nota += 1

        if divPat < 0.5 and divPat > 0:
            nota += 1

        if cresc > 5:
            nota += 1

        if pvp < 2 and pvp > 0:
            nota += 1

        if pl < 15 and pl > 0:
            nota += 1

        if dy > 2.5:
            nota += 1

        if newStock["valorMercado"] < newStock["valorFirma"]:
            nota += 1

        # caso entre mais alguma nota acima, modificar o dividendo abaixo para ter nota máxima de 10
        newStock["score"] = float(nota) / 9.0 * 10.0

        # desconto
        newStock["desconto"] = newStock["valorIntriseco"] - newStock["stockPrice"] if newStock["valorIntriseco"] > 0 else 0

        final_stocks.append(newStock)

    # insere db
    db.insert(final_stocks)
