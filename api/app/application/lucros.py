import logging

from app.application import db

from numpy import percentile
import warnings

warnings.filterwarnings("ignore")


logger = logging.getLogger(__name__)


def safe_div(n, d):
    try:
        r = n / d
    except ZeroDivisionError:
        return 0
    return r


def valida_ultimos_lucros(lucros, ultimos_12m):
    """
    Verifica se os últimos resultados foram positivos
    """
    # os 2 ultimos anos descartando o ultimo
    data_p = sorted(lucros.items(), key=lambda item: item[0], reverse=True)[:2]

    status = True

    # verificar os ultimos anos se tem prejuizo
    count = 0
    counter = 0
    for v in data_p:
        vlr = v[1]

        if vlr < 0 and counter > 0:
            # para o periodo do covid
            count += 1
        counter += 1

    if count > 0:
        logger.info(f"{count} anos com prejuízo")
        status = False

    # os ultimos 3 anos a partir do primeiro
    # verifica se os lucros vem caindo
    lucros_desc, ctrl = 0, 0
    if count == 0:
        data_l = sorted(lucros.items(), key=lambda item: item[0], reverse=False)[-3:]

        ultimo_lucro, ctrl = None, 0
        for v in data_l:
            vlr = v[1]
            ctrl += 1

            # verifica se o lucro vem caindo
            if ultimo_lucro:
                # ex: se 2018 for menor que 2017 (gordura de 15%)
                if vlr < (ultimo_lucro * 0.7):
                    lucros_desc += 1
                    ultimo_lucro = vlr
            else:
                ultimo_lucro = vlr

        # se tem muitos lucros descrescentes
        if lucros_desc == (ctrl - 1):
            status = False
            logger.info(f"{lucros_desc} lucros decrescendo")

        # veririca se o lucro dos ultimos 12m é abaixo do p40 dos ultimos 2 anos fechados
        try:
            ptl = percentile(data_l[-2:], 40)

            if ultimos_12m < ptl:
                status = False
                logger.info(f"Descartando pois lucros de 12m com {ultimos_12m} e p40 {ptl}")
        except Exception:
            logger.exception("Exception")

    return status


def lucro_resultado_geral(data, media):
    # se p50 for menor que zero ou media menor que zero
    try:
        p50 = percentile([x for x in data.values()], 50)
    except:
        logger.info(f"{data} - {media}")

    if p50 < 0:
        logger.info(f"Lucro p50 abaixo de zero {p50}")
        return False
    elif media < 0:
        logger.info(f"Média lucros geral abaixo de zero {media}")
        return False
    return True


def valida_empresa(code):
    lc, media, ultimos_12m = get_lucro_details(code)

    logger.info(code)
    status = valida_ultimos_lucros(lc, ultimos_12m)
    if not status:
        logger.info(f"Descartando {code} pelos últimos lucros")

    if status:
        # somente valida o geral se os ultimos forem positivos
        status = lucro_resultado_geral(lc, media)
        if not status:
            logger.info(f"Descartado {code} pelos lucros históricos negativos")

    return status


def get_lucro_details(code):
    details = db.consulta_detalhes("dre", code)

    lc = {}
    ultimos_12m = None
    for row in details[0]:
        if row["tipo"] in ["Lucro Líquido - (R$) format_quote", "Lucro Líquido - (R$)"]:
            periodo = row["periodo"]
            lucro = row["valor"]
            if periodo == "Últ. 12M":
                ultimos_12m = lucro
            else:
                lc[int(periodo)] = float(lucro)

    values = [x for x in lc.values()]
    media = safe_div(sum(values), len(values))

    return lc, media, ultimos_12m


def check_dre(code):
    """
    Aqui podem ser inseridos outros dados como receita, lucros, etc
    """
    dre = {}
    dre["lucro"], dre["media_lucro"], dre["lucro_12m"] = get_lucro_details(code)

    return dre
