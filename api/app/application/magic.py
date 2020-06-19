from datetime import datetime
import logging
import argparse

import app.application.db as db
from app.application.technical import Technical

from numpy import percentile, median
import math


logger = logging.getLogger(__name__)


def get_result(estrategia, small_caps=False, setor=None):
    performance, value = db.select_rank_magic_formula(estrategia, small_caps)

    p, v, magic_formula, sem_lucro = {}, {}, {}, []

    count = 0
    for row in value:
        code = row[0]
        status = valida_empresa(code)
        if status and code not in sem_lucro:
            v[code] = count
            count += 1
        else:
            sem_lucro.append(code)

    count = 0
    for row in performance:
        code = row[0]
        if code not in sem_lucro:
            p[code] = count
            count += 1

    for code, score in v.items():
        magic_formula[code] = score + p[code]

    ordered = {
        k: v
        for k, v in sorted(
            magic_formula.items(), key=lambda item: item[1], reverse=True
        )
    }
    return ordered


def zero_if_neg(n):
    if n < 0:
        return 0
    return n


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
    for v in data_p:
        vlr = v[1]

        if vlr < 0:
            count += 1

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
                if vlr < (ultimo_lucro * 0.85):
                    lucros_desc += 1
                    ultimo_lucro = vlr
            else:
                ultimo_lucro = vlr

        # se tem muitos lucros descrescentes
        if lucros_desc == (ctrl - 1):
            status = False
            logger.info(f"{lucros_desc} lucros decrescendo")

        # veririca se o lucro dos ultimos 12m é abaixo do p70 dos ultimos 2 anos fechados
        ptl = percentile(data_l[-2:], 62)
        if ultimos_12m < ptl:
            status = False
            logger.info(f"Descartando pois lucros de 12m com {ultimos_12m} e p70 {ptl}")

    return status


def lucro_resultado_geral(data, media):
    # se p50 for menor que zero ou media menor que zero
    p50 = percentile([x for x in data.values()], 50)
    if p50 < 0:
        logger.info(f"Lucro p50 abaixo de zero {p50}")
        return False
    elif media < 0:
        logger.info(f"Média lucros geral abaixo de zero {media}")
        return False
    return True


def valida_empresa(code):
    lc, media, ultimos_12m = get_lucro_details(code)

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
    lucros = db.consulta_detalhes_periodo(code, "lucro")

    lc = {}
    ultimos_12m = None
    for row in lucros:
        tipo = row[0]
        lucro = row[1]
        if tipo == "Últ. 12M":
            ultimos_12m = row[1]
        else:
            lc[int(tipo)] = float(lucro)

    values = [x for x in lc.values()]
    media = safe_div(sum(values), len(values))

    return lc, media, ultimos_12m


def check_dre(code):
    """
    Aqui podem ser inseridos outros dados como receita, lucros, etc
    """
    dre = {}
    dre["lucro"], dre["media_lucro"], dre["lucro_12m"] = get_lucro_details(code=code)

    return dre


def millify(n):
    millnames = ["", " Mil", " Mi", " Bi", " Tri"]

    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))
        ),
    )
    result = n / 10 ** (3 * millidx), millnames[millidx]

    return "{:.1f}{}".format(result[0], result[1])


def pl_setor(code):
    rows = db.pl_setor(code)
    vl = []
    for row in rows:
        vl.append(row[0])

    if vl:
        return percentile(vl, 50)
    return None


def pl_bolsa():
    rows = db.pl_geral()
    vl = []
    for row in rows:
        vl.append(row[0])

    for p in (("p50", 50), ("p90", 90), ("p95", 95)):
        pv = p[1]
        value = percentile(vl, pv)
        print(f"{p[0]} do P/L Geral Bolsa: {value:.2f}")


def format_number(n, repl="-"):
    if n:
        return round(n, 2)
    return repl


def rank(estrategia, small_caps, numero_empresas, setor_especifico):
    log = "Iniciando a análise "
    if estrategia == "ev_ebit_roic":
        log += "usando a estratégia EV/EBIT e ROIC "
    else:
        log += "usando a estratégia P/L e ROE "

    if small_caps:
        log += "para SMALL CAPS"

    logger.info(log)

    magic_result = get_result(estrategia, small_caps)

    l, count, setores_an, = [], 0, {}
    for code, score in magic_result.items():
        d = db.select_details(code)
        setor = d[0][0] if d[0][0] else "-"
        if not setor_especifico or str(setor).lower() == str(setor_especifico).lower():
            details = check_dre(code)

            lucro = millify(details["media_lucro"])

            pvp = format_number(d[0][1], 0)
            ev_ebit = format_number(d[0][2])
            roic = format_number(d[0][3])
            pl = format_number(d[0][4])
            roe = format_number(d[0][5])
            dist_min = format_number(d[0][6], 0)
            preco = format_number(d[0][7])
            intriseco = format_number(d[0][8])
            dy = format_number(d[0][10], 0)
            div_pat = format_number(d[0][11], 0)
            margem = margem = format_number(d[0][12], "-")
            div_ativo = format_number(d[0][14], 0)
            cagr_lucro = format_number(d[0][15], "-")
            cagr_receita = format_number(d[0][16], "-")
            valor_12m = format_number(d[0][17], "-")
            roa = format_number(d[0][19], "-")
            vpa = format_number(d[0][20], "-")

            try:
                pegr = None
                if d[0][4] and d[0][15]:
                    pegr = format_number(float(d[0][4]) / float(d[0][15]))
            except ZeroDivisionError:
                pegr = None

            if setor in setores_an:
                avg_pl = setores_an[setor]
            else:
                avg_pl = format_number(pl_setor(code), "-")
                setores_an[setor] = avg_pl

            technical = Technical.get_indicators(code)
            medias = Technical.get_moving_averages(code)

            l.append(
                [count,
                score,
                code,
                setor,
                ev_ebit,
                roic,
                pl,
                pegr,
                pl_setor(code),
                roe,
                roa,
                pvp,
                margem,
                vpa,
                dy,
                lucro,
                cagr_receita,
                cagr_lucro,
                div_pat,
                div_ativo,
                preco,
                intriseco,
                dist_min,
                valor_12m, 
                technical,
                medias]
            )

            count += 1

            if count == numero_empresas:
                break


    return l


def columns():
    return [
        {"text": "order", "type": "number"},
        {"text": "score", "type": "number"},
        {"text": "code", "type": "string"},
        {"text": "setor", "type": "string"},
        {"text": "ev/ebit", "type": "number"},
        {"text": "roic", "type": "number"},
        {"text": "pl", "type": "number"},
        {"text": "pegr", "type": "number"},
        {"text": "pl_setor", "type": "number"},
        {"text": "roe", "type": "number"},
        {"text": "roa", "type": "number"},
        {"text": "p_vp", "type": "number"},
        {"text": "margem_liquida", "type": "number"},
        {"text": "vpa", "type": "number"},
        {"text": "dy", "type": "number"},
        {"text": "lucro", "type": "string"},
        {"text": "crescimento_receita", "type": "number"},
        {"text": "crescimento_lucro", "type": "number"},
        {"text": "div_pat", "type": "number"},
        {"text": "div_ebit", "type": "number"},
        {"text": "preco", "type": "number"},
        {"text": "valor_intriseco", "type": "number"},
        {"text": "distancia_min", "type": "number"},
        {"text": "valorizacao_12m", "type": "number"},
        {"text": "tecnico", "type": "string"},
        {"text": "medias", "type": "string"},
    ]


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def parse_param():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--ev_ebit",
        type=str2bool,
        nargs="?",
        const=True,
        default=False,
        help="Usa a estratégia pelo EV/EBIT com ROIC",
    )
    parser.add_argument(
        "-p",
        "--pl",
        type=str2bool,
        nargs="?",
        const=True,
        default=False,
        help="Usa a estratégia usando PL e ROE",
    )
    parser.add_argument(
        "-s", "--small_caps", type=str2bool, nargs="?", const=True, default=False
    )
    parser.add_argument("-n", "--numero_empresas", type=int, default=30)
    parser.add_argument("-t", "--setor", type=str, default=None)
    args = parser.parse_args()

    small_caps = args.small_caps
    estrategia = "pl_roe" if args.pl else "ev_ebit_roic"
    numero_empresas = args.numero_empresas
    setor = args.setor

    return (estrategia, small_caps, numero_empresas, setor)
