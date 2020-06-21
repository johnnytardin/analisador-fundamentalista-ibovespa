import logging

import app.application.db as db

import math


logger = logging.getLogger(__name__)


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


def get_lucro_details(code):
    details = db.consulta_detalhes(code, "dre")

    lc = {}
    ultimos_12m = None
    for row in details:
        if row["tipo"] == "Lucro Líquido - (R$)":
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


def format_number(n, repl=None):
    if n:
        return round(float(n), 2)
    return repl


def get_summary(code):
    d = db.select_details(code)

    details = check_dre(code)

    setor = d[0][0] if d[0][0] else "-"
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
    margem = format_number(d[0][12])
    div_ativo = format_number(d[0][14], 0)
    cagr_lucro = format_number(d[0][15])
    cagr_receita = format_number(d[0][16])
    valor_12m = format_number(d[0][17])
    roa = format_number(d[0][19])
    vpa = format_number(d[0][20])

    pegr = None
    try:
        if d[0][4] and d[0][15]:
            pegr = format_number(float(d[0][4]) / float(d[0][15]))
    except ZeroDivisionError:
        pass

    # monta a resposta
    summary = [
        setor,
        lucro,
        pvp,
        ev_ebit,
        roic,
        pl,
        roe,
        dist_min,
        preco,
        intriseco,
        dy,
        div_pat,
        margem,
        div_ativo,
        cagr_lucro,
        cagr_receita,
        valor_12m,
        roa,
        vpa,
        pegr,
    ]

    return summary


def columns():
    return [
        {"text": "setor", "type": "string"},
        {"text": "lucro", "type": "string"},
        {"text": "pvp", "type": "number"},
        {"text": "ev_ebit", "type": "number"},
        {"text": "roic", "type": "number"},
        {"text": "pl", "type": "number"},
        {"text": "roe", "type": "number"},
        {"text": "roe", "type": "number"},
        {"text": "dist_min", "type": "number"},
        {"text": "preco", "type": "number"},
        {"text": "intriseco", "type": "number"},
        {"text": "dy", "type": "number"},
        {"text": "div_pat", "type": "number"},
        {"text": "margem", "type": "number"},
        {"text": "div_ativo", "type": "number"},
        {"text": "cagr_lucro", "type": "number"},
        {"text": "cagr_receita", "type": "number"},
        {"text": "valor_12m", "type": "number"},
        {"text": "roa", "type": "number"},
        {"text": "vpa", "type": "number"},
    ]
