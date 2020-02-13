from datetime import datetime

import db
import reports.db as reportsdb

from numpy import percentile
from tabulate import tabulate
import math

DEBUG = False


def get_result(tipo="todos"):
    if tipo == "financeiro":
        print("Score para o setor Financeiro")

        performance = db.select_roe()
        value = db.select_pl()
    else:
        print("Score para todos os setores")

        performance = db.select_roic()
        value = db.select_ev_ebit()

    p, v, magic_formula, sem_lucro = {}, {}, {}, []

    count = 0
    for row in value:
        code = row[0]
        _, _, status = lucro_liquido(code)
        if status in [0, -1] and code not in sem_lucro:
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


def lucro_liquido(code=None, cnpj=None):
    if not cnpj:
        try:
            cnpj, _ = db.stock_code_cnpj(code)
        except TypeError:
            print(f"WARNING - CADASTRO - Falha coletando para {code}. CNPJ: {cnpj}")
            return ({}, -1, -1)

    # if code == 'PNVL3':
    #    import ipdb; ipdb.set_trace()

    rows = reportsdb.consulta_dre(cnpj, "lucro")

    l = {}
    for row in rows:
        tipo, ano, lucro, escala = row
        if tipo == "PENÚLTIMO":
            a = int(ano)
            ano = a - 1

        if escala == "MILHAR":
            lucro *= 1000

        l[int(ano)] = float(lucro)

    if l:
        values = [x for x in l.values()]
        media = safe_div(sum(values), len(values))
    else:
        media = None

    try:
        status = 0
        if percentile([x for x in l.values()], 20) < 0 or media < 0:
            status = 1
    except IndexError:
        if DEBUG:
            print(
                f"WARNING - CÁLCULO - Falha calculando o lucro para {code}. CNPJ: {cnpj}"
            )
        status = -1

    return l, media, status


def dividendos(cnpj):
    rows = reportsdb.consulta_dre(cnpj, "dividendos")

    if rows:
        _, ano, vlr, escala = rows[-1]
        if escala == "MILHAR":
            vlr *= 1000
    else:
        return {}

    return {int(ano): float(vlr)}


def juros_capital_proprio(cnpj):
    rows = reportsdb.consulta_dre(cnpj, "juros_capital_proprio")

    if rows:
        _, ano, vlr, escala = rows[-1]
        if escala == "MILHAR":
            vlr *= 1000
    else:
        return {}

    return {int(ano): float(vlr)}


def get_dre_details(cnpj):
    dre = {}
    dre["lucro"], dre["media_lucro"], _ = lucro_liquido(cnpj=cnpj)
    for ano, value in dividendos(cnpj).items():
        dre["dividendos"] = (ano, value)

    for ano, value in juros_capital_proprio(cnpj).items():
        dre["juros_capital"] = (ano, value)

    if dre["lucro"]:
        dre["proventos"] = (
            dre["dividendos"][0],
            dre["dividendos"][1] + dre["juros_capital"][1],
        )

        dre["payout"] = int(
            safe_div(dre["proventos"][1], dre["lucro"][dre["proventos"][0]]) * 100
        )
    else:
        dre["payout"] = None
        dre["proventos"] = None

    return dre


def check_cnpj(cnpj):
    try:
        int(cnpj.replace(".", "").replace("/", "").replace("-", ""))
    except ValueError:
        print(f"CNPJ {cnpj} inválido")
        raise


def check_dre(code):
    try:
        cnpj, _ = db.stock_code_cnpj(code)
        check_cnpj(cnpj)

        dt = get_dre_details(cnpj)
    except TypeError:
        print(f"WARNING - CADASTRO - Falha coletando o CNPJ para {code}")
        return ("", {})
    except ValueError:
        return ("", {})

    return (cnpj, dt)


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


def main():
    print(chr(27) + "[2J")

    for t in ["financeiro", "todos"]:
        magic_result = get_result(t)

        l, count, cnpjs_analisados = [], 0, []
        for code, score in magic_result.items():
            cnpj, details = check_dre(code)
            d = db.select_details(code)

            if details:
                if details["media_lucro"]:
                    lucro = millify(details["media_lucro"])
                else:
                    lucro = "*"
                    code = f"{code}*"

                if details["payout"]:
                    payout = details["payout"]
                else:
                    payout = "*"
            else:
                lucro = "*"
                payout = "*"

            l.append(
                [
                    count,
                    score,
                    code,
                    d[0][0][0:20] if d[0][0] else "-",
                    round(d[0][1], 2) if d[0][1] else "-",
                    round(d[0][2], 2) if d[0][2] else "-",
                    round(d[0][3], 2) if d[0][3] else "-",
                    round(d[0][4], 2) if d[0][4] else "-",
                    round(d[0][5], 2) if d[0][5] else "-",
                    round(d[0][6], 2) if d[0][6] else "-",
                    round(d[0][7], 2) if d[0][7] else "-",
                    round(d[0][8], 2) if d[0][8] else d[0][8],
                    round(d[0][9], 2) if d[0][9] else d[0][9],
                    round(d[0][10], 2) if d[0][10] else d[0][10],
                    round(d[0][11], 2) if d[0][11] else d[0][11],
                    round(d[0][12], 2) if d[0][12] else d[0][12],
                    round(d[0][13], 2) if d[0][13] else d[0][13],
                    round(d[0][14], 2) if d[0][14] else d[0][14],
                    lucro,
                    payout,
                ]
            )
            if cnpj not in cnpjs_analisados:
                cnpjs_analisados.append(cnpj)

            count += 1

            if len(cnpjs_analisados) == 30:
                break

        print(
            tabulate(
                l,
                headers=[
                    "Order",
                    "Score",
                    "CODE",
                    "Setor",
                    "P/VP",
                    "EV/EBIT",
                    "ROIC%",
                    "PL",
                    "ROE%",
                    "D.Min.%",
                    "Preço",
                    "Vlr.Intr.",
                    "Desc.%",
                    "DY%",
                    "Cr.(5a)%",
                    "D.Br/Patr",
                    "M.Liq.%",
                    "LPA",
                    "Avg. Luc.",
                    "Payout%",
                ],
                tablefmt="orgtbl",
            )
        )
        print("* Indicam algum erro para calcular.")


if __name__ == "__main__":
    main()
