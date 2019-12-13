import re
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict


def get_data(*args, **kwargs):
    url = 'http://www.fundamentus.com.br/resultado.php'
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min': '',
            'pl_max': '',
            'pvp_min': '',
            'pvp_max': '',
            'psr_min': '',
            'psr_max': '',
            'divy_min': '',
            'divy_max': '',
            'pativos_min': '',
            'pativos_max': '',
            'pcapgiro_min': '',
            'pcapgiro_max': '',
            'pebit_min': '',
            'pebit_max': '',
            'fgrah_min': '',
            'fgrah_max': '',
            'firma_ebit_min': '',
            'firma_ebit_max': '',
            'margemebit_min': '',
            'margemebit_max': '',
            'margemliq_min': '',
            'margemliq_max': '',
            'liqcorr_min': '',
            'liqcorr_max': '',
            'roic_min': '',
            'roic_max': '',
            'roe_min': '',
            'roe_max': '',
            'liq_min': '',
            'liq_max': '',
            'patrim_min': '',
            'patrim_max': '',
            'divbruta_min': '',
            'divbruta_max': '',
            'tx_cresc_rec_min': '',
            'tx_cresc_rec_max': '',
            'setor': '',
            'negociada': 'ON',
            'ordem': '1',
            'x': '28',
            'y': '16'}

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    reg = re.findall(pattern, content)[0]
    page = fragment_fromstring(reg)
    lista = OrderedDict()

    stocks = page.xpath('tbody')[0].findall("tr")

    for i in range(0, len(stocks)):
        lista[i] = {
            stocks[i].getchildren()[0][0].getchildren()[0].text: {
               'cotacao': stocks[i].getchildren()[1].text,
               'P/L': stocks[i].getchildren()[2].text,
               'P/VP': stocks[i].getchildren()[3].text,
               'PSR': stocks[i].getchildren()[4].text,
               'DY': stocks[i].getchildren()[5].text,
               'P/Ativo': stocks[i].getchildren()[6].text,
               'P/Cap.Giro': stocks[i].getchildren()[7].text,
               'P/EBIT': stocks[i].getchildren()[8].text,
               'P/Ativ.Circ.Liq.': stocks[i].getchildren()[9].text,
               'EV/EBIT': stocks[i].getchildren()[10].text,
               'EV/EBITDA': stocks[i].getchildren()[11].text,
               'Mrg.Ebit.': stocks[i].getchildren()[12].text,
               'Mrg.Liq.': stocks[i].getchildren()[13].text,
               'Liq.Corr.': stocks[i].getchildren()[14].text,
               'ROIC': stocks[i].getchildren()[15].text,
               'ROE': stocks[i].getchildren()[16].text,
               'Liq.2m.': stocks[i].getchildren()[17].text,
               'Pat.Liq': stocks[i].getchildren()[18].text,
               'Div.Brut/Pat.': stocks[i].getchildren()[19].text,
               'Cresc.5a': stocks[i].getchildren()[20].text
               }
            }

    return lista


def get_specific_data(stock):
    url = "http://www.fundamentus.com.br/detalhes.php?papel=" + stock
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]
    
    # Get data from site
    link = opener.open(url, urllib.parse.urlencode({}).encode('UTF-8'))
    content = link.read().decode('ISO-8859-1')

    # Get all table instances
    pattern = re.compile('<table class="w728">.*</table>', re.DOTALL)
    reg = re.findall(pattern, content)[0]
    reg = "<div>" + reg + "</div>"
    page = fragment_fromstring(reg)
    all_data = {}

    # There is 5 tables with tr, I will get all trs
    all_trs = []
    all_tables = page.xpath("table")

    for i in range(0, len(all_tables)):
        all_trs = all_trs + all_tables[i].findall("tr")

    # Run through all the trs and get the label and the
    # data for each line
    for tr_index in range(0, len(all_trs)):
        tr = all_trs[tr_index]
        # Get into td
        all_tds = tr.getchildren()
        for td_index in range(0, len(all_tds)):
            td = all_tds[td_index]


            label = ""
            data = ""

            # The page has tds with contents and some 
            # other with not
            if (td.get("class").find("label") != -1):
                # We have a label
                for span in td.getchildren():
                    if (span.get("class").find("txt") != -1):
                        label = span.text

                # If we did find a label we have to look 
                # for a value 
                if (label and len(label) > 0):
                    next_td = all_tds[td_index + 1]

                    if (next_td.get("class").find("data") != -1):
                        # We have a data
                        for span in next_td.getchildren():
                            if (span.get("class").find("txt") != -1):
                                if (span.text):
                                    data = span.text
                                else:
                                    # If it is a link
                                    span_children = span.getchildren()
                                    if (span_children and len(span_children) > 0):
                                        data = span_children[0].text

                                # Include into dict
                                all_data[label] = data

                                # Erase it
                                label = ""
                                data = ""

    return all_data
