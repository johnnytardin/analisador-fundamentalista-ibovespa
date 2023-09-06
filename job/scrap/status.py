import logging
from datetime import datetime

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service


pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


DADOS = {}


def element(driver, x_path):
    try:
        indicadores = driver.find_element(By.XPATH, x_path)
    except Exception as e:
        print(f"Falha coletando o xpath {x_path}")
        return ""

    if indicadores:
        return indicadores.text
    return ""


def x_paths():
    return [
        # INDICADORES DE VALUATION
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[2]/div/div/strong""",
            "P/L",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[3]/div/div/strong""",
            "PEG RATIO",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[4]/div/div/strong""",
            "P/VP",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[5]/div/div/strong""",
            "EV/EBITDA",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[6]/div/div/strong""",
            "EV/EBIT",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[7]/div/div/strong""",
            "P/EBITDA",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[8]/div/div/strong""",
            "P/EBIT",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[9]/div/div/strong""",
            "VPA",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[10]/div/div/strong""",
            "P/ATIVO",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[11]/div/div/strong""",
            "LPA",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[12]/div/div/strong""",
            "PSR",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[13]/div/div/strong""",
            "P/CAP.GIRO",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[14]/div/div/strong""",
            "P/ATIVO CIRC LIQ",
        ),
        # INDICADORES DE EFICIÊNCIA
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[3]/div/div[1]/div/div/strong""",
            "MARGEM BRUTA",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[3]/div/div[2]/div/div/strong""",
            "MARGEM EBITDA",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[3]/div/div[3]/div/div/strong""",
            "MARGEM EBIT",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[3]/div/div[4]/div/div/strong""",
            "MARGEM LÍQUIDA",
        ),
        # INDICADORES DE RENTABILIDADE
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[4]/div/div[1]/div/div/strong""",
            "ROE",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[4]/div/div[2]/div/div/strong""",
            "ROA",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[4]/div/div[3]/div/div/strong""",
            "ROIC",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[4]/div/div[4]/div/div/strong""",
            "GIRO ATIVOS",
        ),
        # INDICADORES DE CRESCIMENTO
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[5]/div/div[1]/div/div/strong""",
            "CAGR RECEITAS 5 ANOS",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[5]/div/div[2]/div/div/strong""",
            "CAGR LUCROS 5 ANOS",
        ),
        # INDICADORES DE ENDIVIDAMENTO
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[1]/div/div/strong""",
            "DÍVIDA LÍQUIDA / PATRIMÔNIO LIQ",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[2]/div/div/strong""",
            "DÍVIDA LÍQUIDA / EBITDA",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[3]/div/div/strong""",
            "DÍVIDA LÍQUIDA / EBIT",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[4]/div/div/strong""",
            "PL / ATIVOS",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[5]/div/div/strong""",
            "PASSIVOS / ATIVOS",
        ),
        (
            """/html/body/main/div[2]/div/div[8]/div[2]/div/div[2]/div/div[6]/div/div/strong""",
            "LIQUIDEZ CORRENTE",
        ),
        # PREÇO
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
            """/html/body/main/div[2]/div/div[1]/div/div[5]/div/div[1]/strong""",
            "VALORIZAÇÃO (12M)",
        ),
        (
            """/html/body/main/div[2]/div/div[1]/div/div[5]/div/div[2]/div/span[2]/b""",
            "VALORIZAÇÃO (MÊS ATUAL)",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div/div[3]/div/div/div/strong""",
            "LIQUIDEZ MÉDIA DIÁRIA",
        ),
        # SETOR DE ATUAÇÃO
        (
            """/html/body/main/div[5]/div[1]/div/div[3]/div/div[1]/div/div/div/a/strong""",
            "SETOR DE ATUAÇÂO",
        ),
        (
            """/html/body/main/div[5]/div[1]/div/div[3]/div/div[2]/div/div/div/a/strong""",
            "SUBSETOR DE ATUAÇÂO",
        ),
        (
            """/html/body/main/div[5]/div[1]/div/div[3]/div/div[3]/div/div/div/a/strong""",
            "SEGMENTO DE ATUAÇÂO",
        ),
        # DETALHES DA EMPRESA
        (
            """/html/body/main/div[5]/div[1]/div/div[2]/div[7]/div/div/strong""",
            "VALOR DE MERCADO",
        ),
        (
            """/html/body/main/div[5]/div[1]/div/div[2]/div[11]/div/div/strong""",
            "FREE FLOAT",
        ),
        (
            """/html/body/main/div[2]/div/div[5]/div/div/div[2]/div/div/div/strong""",
            "TAG ALONG",
        ),
        (
            """/html/body/main/div[5]/div[1]/div/div[2]/div[10]/div/div/strong""",
            "SEGMENTO DE LISTAGEM",
        ),
        (
            """/html/body/main/div[5]/div[1]/div/div[1]/div[2]/div[1]/strong""",
            "RECUPERACAO JUDICIAL",
        ),
        # ALUGUEL
        (
            """/html/body/main/div[2]/div/div[8]/div/div[2]/div[1]/div/div[1]/strong""",
            "TAXA ALUGUEL TOMADOR",
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
    dre_dt = df[3].to_dict()

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
        options.add_argument('--headless')
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        )
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_script_timeout(60)
        driver.get(url)
        # scroll pois a pagina carrega dinamicamente
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/main/div[7]/div/div/div[2]/div[1]/div/table/tbody/tr[1]/td[2]/span",
                )
            )
        )

        dre(driver, stock)
        fundamentus(driver)

    except Exception as err:
        logging.exception(
            "Falha coletando os dados na stock para {}. Causa: {}".format(stock, err),
            exc_info=True,
        )
        return {}
    finally:
        driver.close()
        driver.quit()

    return DADOS
