from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import pandas as pd


DADOS = {}


def element(driver, x_path):
    indicadores = driver.find_elements_by_xpath(x_path)[0]
    return indicadores.text


def x_paths():
    return [
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[3]/div/div/strong""",
            "P/VP",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[1]/div/div/strong""",
            "P/L",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[5]/div/div/strong""",
            "P/EBITDA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[6]/div/div/strong""",
            "P/EBIT",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[8]/div/div/strong""",
            "P/ATIVO",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[2]/div/div/strong""",
            "EV/EBITDA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[4]/div/div/strong""",
            "EV/EBIT",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[10]/div/div/strong""",
            "PSR",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[11]/div/div/strong""",
            "P/CAP.GIRO",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[12]/div/div/strong""",
            "P/ATIVO CIRC LIQ",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[3]/div/div[1]/div/div/strong""",
            "MARGEM BRUTA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[3]/div/div[2]/div/div/strong""",
            "MARGEM EBITDA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[3]/div/div[3]/div/div/strong""",
            "MARGEM EBIT",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[3]/div/div[4]/div/div/strong""",
            "MARGEM LÍQUIDA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[4]/div/div[4]/div/div/strong""",
            "GIRO ATIVOS",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[4]/div/div[1]/div/div/strong""",
            "ROE",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[4]/div/div[2]/div/div/strong""",
            "ROA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[4]/div/div[3]/div/div/strong""",
            "ROIC",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[9]/div/div/strong""",
            "LPA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[7]/div/div/strong""",
            "VPA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[2]/div/div[1]/div/div/strong""",
            "DÍVIDA LÍQUIDA / PATRIMÔNIO",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[2]/div/div[2]/div/div/strong""",
            "DÍVIDA LÍQUIDA / EBITDA",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[2]/div/div[3]/div/div/strong""",
            "DÍVIDA LÍQUIDA / EBIT",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[1]/div/div[8]/div/div/strong""",
            "PATRIMÔNIO / ATIVOS",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[2]/div/div[5]/div/div/strong""",
            "PASSIVOS / ATIVOS",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[2]/div/div[6]/div/div/strong""",
            "LIQUIDEZ CORRENTE",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[5]/div/div[1]/div/div/strong""",
            "CAGR RECEITAS 5 ANOS",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div[5]/div/div[2]/div/div/strong""",
            "CAGR LUCROS 5 ANOS",
        ),
        (
            """/html/body/main/div[2]/div/div[1]/div/div[1]/div/div[1]/strong""",
            "VALOR ATUAL",
        ),
        (
            """/html/body/main/div[2]/div/div[1]/div/div[2]/div/div[1]/strong""",
            "MIN. 52 SEMANAS",
        ),
        (
            """/html/body/main/div[2]/div/div[1]/div/div[3]/div/div[1]/strong""",
            "MÁX. 52 SEMANAS",
        ),
        (
            """/html/body/main/div[2]/div/div[1]/div/div[4]/div/div[1]/strong""",
            "DIVIDEND YIELD",
        ),
        (
            """/html/body/main/div[3]/div/div[2]/div[7]/div/div/strong""",
            "VALOR DE MERCADO",
        ),
        (
            """/html/body/main/div[2]/div/div[1]/div/div[5]/div/div[1]/strong""",
            "VALORIZAÇÃO (12M)",
        ),
        (
            """/html/body/main/div[2]/div/div[1]/div/div[5]/div/div[2]/div/span[2]/b""",
            "VALORIZAÇÃO (MÊS ATUAL)",
        ),
        (
            """/html/body/main/div[2]/div/div[3]/div/div/div[3]/div/div/div/strong""",
            "LIQUIDEZ MÉDIA DIÁRIA",
        ),
        (
            """/html/body/main/div[3]/div/div[3]/div/div[1]/div/div/div/a/strong""",
            "SETOR DE ATUAÇÂO",
        ),
        (
            """/html/body/main/div[3]/div/div[3]/div/div[2]/div/div/div/a/strong""",
            "SUBSETOR DE ATUAÇÂO",
        ),
        (
            """/html/body/main/div[3]/div/div[3]/div/div[3]/div/div/div/a/strong""",
            "SEGMENTO DE ATUAÇÂO",
        ),
        ("""/html/body/main/div[3]/div/div[2]/div[11]/div/div/strong""", "FREE FLOAT",),
        (
            """/html/body/main/div[2]/div/div[3]/div/div/div[2]/div/div/div/strong""",
            "TAG ALONG",
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


def anos_anteriores():
    """
    para controlar os valores do dict para dados de dre
    string pois o dic vindo do pandas esta nesse formato
    """
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
        driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
        driver.get(url)

        dre(driver, stock)
        fundamentus(driver)
    except Exception as err:
        print("Falha coletando os dados na stock para {}. Causa: {}".format(stock, err))
        return {}
    finally:
        driver.close()
    return DADOS
