import logging

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
        (
            """/html/body/main/div[3]/ul/li[5]/span[2]""",
            "recomendacao"
        ),
        (
            """/html/body/main/div[3]/ul/li[4]/span[2]""",
            "risco"
        ),
    ]


def get_data(driver):
    for path_data in x_paths():
        d = element(driver, path_data[0])
        DADOS[path_data[1]] = d


def get_recommendation(stock):
    try:
        url = "https://conteudos.xpi.com.br/acoes/{}".format(stock.lower())
        print("url", url)
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

        get_data(driver)

    except Exception as err:
        logging.exception(
            "recommendation - Falha coletando os dados na stock para {}. Causa: {}".format(stock, err),
            exc_info=True,
        )
        return {}
    finally:
        driver.close()
        driver.quit()

    return DADOS
