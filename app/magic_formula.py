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
        _, _, status, _ = lucro_liquido(code)
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


def lucro_ultimos_resultados(data):
    """
    Verifica se os últimos resultados foram positivos
    """
    # os 2 ultimos anos a partir do ultimo
    data_p = sorted(data.items(), key=lambda item: item[0], reverse=True)[:2]

    count = 0
    for v in data_p:
        vlr = v[1]

        if vlr < 0:
            count += 1

    # os ultimos 3 anos a partir do primeiro
    lucros_desc, ctrl, status, diff_geral = 0, 0, True, 0
    if count == 0:
        data_l = sorted(data.items(), key=lambda item: item[0], reverse=False)[-3:]

        ultimo_lucro, ctrl = None, 0
        for v in data_l:
            vlr = v[1]
            ctrl += 1

            # verifica se o lucro vem caindo
            if ultimo_lucro:
                # ex: se 2018 for menor que 2017 (gordura de 10%)
                if vlr < (ultimo_lucro * 0.85):
                    lucros_desc += 1
                    ultimo_lucro = vlr
            else:
                ultimo_lucro = vlr

        # remove o ultimo ano
        d1 = sorted(data.items(), key=lambda item: item[0], reverse=True)[1:]
        p80 = percentile([x[1] for x in d1], 80)
        diff_geral = safe_div(data_l[-1][1] - p80, data_l[-1][1])
        if diff_geral <= -0.30:
            status = False

    if count > 0 or not status or lucros_desc == (ctrl - 1):
        return 1, diff_geral
    return 0, diff_geral


def lucro_resultado_geral(data, media):
    if percentile([x for x in data.values()], 30) < 0 or media < 0:
        return 1
    return 0


def lucro_liquido(code=None, cnpj=None):
    if not cnpj:
        try:
            cnpj, _ = db.stock_code_cnpj(code)
        except TypeError:
            print(f"WARNING - CADASTRO - Falha coletando para {code}. CNPJ: {cnpj}")
            return ({}, -1, -1)

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

        status, taxa_cres_lc = lucro_ultimos_resultados(l)
        if status == 0:
            # somente valida o geral se os ultimos forem positivos
            status = lucro_resultado_geral(l, media)
    else:
        if DEBUG:
            print(f"WARNING - Não existem dados para {code}. CNPJ: {cnpj}")
        media = None
        status = -1
        taxa_cres_lc = 0

    return l, media, status, taxa_cres_lc * 100


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
    dre["lucro"], dre["media_lucro"], _, dre["taxa_cres_lc"] = lucro_liquido(cnpj=cnpj)
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


def pl_setor(code):
    avg = db.pl_setor(code)
    vl = []
    for row in avg:
        vl.append(row[0])

    if vl:
        return percentile(vl, 50)
    return None


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


def format_number(n, repl="-"):
    if n:
        return round(n, 2)
    return repl


def main():
    print(chr(27) + "[2J")

    for t in ["financeiro", "todos"]:
        magic_result = get_result(t)

        l, count, cnpjs_analisados, setores_an = [], 0, [], {}
        for code, score in magic_result.items():
            cnpj, details = check_dre(code)
            d = db.select_details(code)

            new_code = None
            if details:
                if details["media_lucro"]:
                    lucro = millify(details["media_lucro"])
                else:
                    lucro = "*"
                    new_code = f"{code}*"

                if details["payout"]:
                    payout = details["payout"]
                else:
                    payout = "*"

                if details["taxa_cres_lc"]:
                    taxa_cres_lc = format_number(details["taxa_cres_lc"])
                else:
                    taxa_cres_lc = "*"
            else:
                lucro = "*"
                payout = "*"

            setor = d[0][0][0:12] if d[0][0] else "-"
            pvp = format_number(d[0][1], 0)
            ev_ebit = format_number(d[0][2])
            roic = format_number(d[0][3])
            pl = format_number(d[0][4])
            roe = format_number(d[0][5])
            dist_min = format_number(d[0][6])
            preco = format_number(d[0][7])
            intriseco = format_number(d[0][8])
            dy = format_number(d[0][10], 0)
            cresc = format_number(d[0][11], "-")
            div_pat = format_number(d[0][12], 0)
            margem = margem = format_number(d[0][13], "-")
            lpa = format_number(d[0][14], 0)
            div_ativo = format_number(d[0][15], 0)

            if setor in setores_an:
                avg_pl = setores_an[setor]
            else:
                avg_pl = format_number(pl_setor(code), "-")
                setores_an[setor] = avg_pl

            l.append(
                [
                    count,
                    score,
                    new_code if new_code else code,
                    setor,
                    ev_ebit,
                    roic,
                    pl,
                    avg_pl,
                    roe,
                    pvp,
                    margem,
                    lpa,
                    dy,
                    lucro,
                    taxa_cres_lc,
                    cresc,
                    div_pat,
                    div_ativo,
                    payout,
                    preco,
                    intriseco,
                    dist_min,
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
                    "Ord.",
                    "Scr",
                    "CODE",
                    "St",
                    "EV/EBIT",
                    "ROIC%",
                    "PL",
                    "PL/S",
                    "ROE%",
                    "P/VP",
                    "M.Lq.%",
                    "LPA",
                    "DY%",
                    "Avg. Luc.",
                    "Cr.Luc.%",
                    "Cr(5a)%",
                    "Div/Pt",
                    "Div/At.",
                    "Py%",
                    "Pr",
                    "Intr.",
                    "Dist.%",
                ],
                tablefmt="orgtbl",
            )
        )
        print("* Indicam algum erro para calcular.")


if __name__ == "__main__":
    main()
