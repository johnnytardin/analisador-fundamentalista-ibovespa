from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


DADOS = {}


def element(driver, x_path):
    indicadores = driver.find_elements_by_xpath(x_path)[0]
    return indicadores.text


def x_paths():
    return [
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[1]/div/div/strong""", "P/VP"),
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[2]/div/div/strong""", "P/L"),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[3]/div/div/strong""",
            "P/EBITDA",
        ),
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[4]/div/div/strong""", "P/EBIT"),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[5]/div/div/strong""",
            "P/ATIVO",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[6]/div/div/strong""",
            "EV/EBITDA",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[7]/div/div/strong""",
            "EV/EBIT",
        ),
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[8]/div/div/strong""", "PSR"),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[9]/div/div/strong""",
            "P/CAP.GIRO",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[10]/div/div/strong""",
            "P/ATIVO CIRC LIQ",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[11]/div/div/strong""",
            "MARGEM BRUTA",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[12]/div/div/strong""",
            "MARGEM EBITDA",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[13]/div/div/strong""",
            "MARGEM EBIT",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[14]/div/div/strong""",
            "MARGEM LÍQUIDA",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[15]/div/div/strong""",
            "GIRO ATIVOS",
        ),
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[16]/div/div/strong""", "ROE"),
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[17]/div/div/strong""", "ROA"),
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[18]/div/div/strong""", "ROIC"),
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[19]/div/div/strong""", "LPA"),
        ("""//*[@id="main-2"]/div[2]/div/div[4]/div/div[20]/div/div/strong""", "VPA"),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[21]/div/div/strong""",
            "DÍVIDA LÍQUIDA / PATRIMÔNIO",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[22]/div/div/strong""",
            "DÍVIDA LÍQUIDA / EBITDA",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[23]/div/div/strong""",
            "DÍVIDA LÍQUIDA / EBIT",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[24]/div/div/strong""",
            "PATRIMÔNIO / ATIVOS",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[25]/div/div/strong""",
            "PASSIVOS / ATIVOS",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[26]/div/div/strong""",
            "LIQUIDEZ CORRENTE",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[27]/div/div/strong""",
            "CAGR RECEITAS 5 ANOS",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[4]/div/div[28]/div/div/strong""",
            "CAGR LUCROS 5 ANOS",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong""",
            "VALOR ATUAL",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[1]/div/div[2]/div/div[1]/strong""",
            "MIN. 52 SEMANAS",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[1]/div/div[3]/div/div[1]/strong""",
            "MÁX. 52 SEMANAS",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[1]/div/div[4]/div/div[1]/strong""",
            "DIVIDEND YIELD",
        ),
        (
            """//*[@id="company-section"]/div/div[2]/div[7]/div/div/strong""",
            "VALOR DE MERCADO",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[1]/div/div[5]/div/div[1]/strong""",
            "VALORIZAÇÃO (12M)",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[1]/div/div[5]/div/div[2]/div/span[2]/b""",
            "VALORIZAÇÃO (MÊS ATUAL)",
        ),
        (
            """//*[@id="main-2"]/div[2]/div/div[3]/div/div/div[3]/div/div/div/strong""",
            "LIQUIDEZ MÉDIA DIÁRIA",
        ),
        (
            """//*[@id="company-section"]/div/div[2]/div[1]/div/div/strong""",
            "PATRIMÔNIO LÍQUIDO",
        ),
        (
            """//*[@id="company-section"]/div/div[3]/div/div[1]/div/div/div/a/strong""",
            "SETOR DE ATUAÇÂO",
        ),
        (
            """//*[@id="company-section"]/div/div[3]/div/div[2]/div/div/div/a/strong""",
            "SUBSETOR DE ATUAÇÂO",
        ),
        (
            """//*[@id="company-section"]/div/div[3]/div/div[3]/div/div/div/a/strong""",
            "SEGMENTO DE ATUAÇÂO",
        ),
    ]


def fundamentus(driver):
    for path_data in x_paths():
        d = element(driver, path_data[0])
        DADOS[path_data[1]] = d


def normalize_money(value):
    try:
        return float(value)
    except ValueError:
        vlr = (
            value.replace(" ", "")
            .replace("M", "")
            .replace("K", "")
            .replace("B", "")
            .replace(".", "")
            .replace(",", ".")
        )
        if value.endswith("B"):
            return float(vlr) * 1000000000
        elif value.endswith("M"):
            return float(vlr) * 1000000
        elif value.endswith("K"):
            return float(vlr) * 1000
        elif vlr == "-":
            return None


def lucro(driver):
    x_path = """//*[@id="contabil-section"]/div/div/div[2]/div[1]/div/table/tbody/tr[10]/td[2]/span"""
    indicadores = driver.find_elements_by_xpath(x_path)[0]
    DADOS["LUCRO LIQUIDO 12M"] = normalize_money(indicadores.text)

    lucro_ano = {}
    x_path = """//*[@id="contabil-section"]/div/div/div[2]/div[1]/div/table/tbody/tr[10]/td[4]/span"""
    indicadores = driver.find_elements_by_xpath(x_path)[0]
    lucro_ano["ano_1"] = normalize_money(indicadores.text)

    x_path = """//*[@id="contabil-section"]/div/div/div[2]/div[1]/div/table/tbody/tr[10]/td[7]/span"""
    indicadores = driver.find_elements_by_xpath(x_path)[0]
    lucro_ano["ano_2"] = normalize_money(indicadores.text)

    DADOS["LUCRO POR ANO"] = lucro_ano


def anos_anteriores():
    """
    para controlar os valores do dict para dados de dre
    string pois o dic vindo do pandas esta nesse formato
    """
    from datetime import datetime

    anos = [str(datetime.now().year)]

    for r in range(1, 11):
        anos.append(str(int(anos[0]) - r))

    return anos


def dre(driver, stock):
    df = pd.read_html(driver.page_source, decimal=",", thousands=".")
    dre_dt = df[1].to_dict()

    anos_considerar = anos_anteriores()

    d = []
    for indice, tipo in dre_dt["#"].items():
        for periodo, valor in dre_dt.items():
            if periodo in anos_considerar or periodo.startswith("Últ. 12M") == 1:
                if periodo.startswith("Últ. 12M"):
                    periodo = "Últ. 12M"
                d.append(
                    {
                        "stock": stock,
                        "tipo": tipo,
                        "periodo": periodo,
                        "valor": normalize_money(valor[indice]),
                    }
                )

    DADOS["dre"] = d


def get_specific_data(stock):
    try:
        url = "https://statusinvest.com.br/acoes/{}".format(stock.lower())
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(
            "/usr/lib/chromium-browser/chromedriver", chrome_options=options
        )
        driver.get(url)

        dre(driver, stock)
        fundamentus(driver)
        lucro(driver)
    except Exception as err:
        print("Falha coletando os dados na stock para {}. Causa: {}".format(stock, err))
        return {}
    finally:
        driver.close()
    return DADOS
