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
        print(code)
        _, _, status, _ = valida_empresa(code)
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


def valida_ultimos_resultados(lucros, ultimos_12m):
    """
    Verifica se os últimos resultados foram positivos
    """
    # os 2 ultimos anos descartando o ultimo
    data_p = sorted(lucros.items(), key=lambda item: item[0], reverse=True)[:2]

    # verificar os ultimos anos se tem prejuizo
    count = 0
    for v in data_p:
        vlr = v[1]

        if vlr < 0:
            count += 1

    # os ultimos 3 anos a partir do primeiro
    # verifica se os lucros vem caindo
    lucros_desc, ctrl, status, diff_geral = 0, 0, True, 0
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

        # veririca se o ultimo lucro é muito abaixo do do normal
        d1 = sorted(lucros.items(), key=lambda item: item[0], reverse=True)[1:]
        p = percentile([x[1] for x in d1], 70)
        diff_geral = safe_div(ultimos_12m - p, data_l[-1][1])
        if diff_geral <= -0.30:
            print("menor geral")
            status = False

    # valida a saida
    #TODO: verificar se um somente é válido
    if count > 0 or not status or lucros_desc == (ctrl - 1):
        return 1
    return 0


def lucro_resultado_geral(data, media):
    # se p50 for menor que zero ou media menor que zero
    if percentile([x for x in data.values()], 50) < 0 or media < 0:
        return 1
    return 0


def valida_empresa(code):
    lucros = reportsdb.consulta_detalhes_periodo(code, "lucro")

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

    status = valida_ultimos_resultados(lc, ultimos_12m)
    if status == 1:
        print(f"Descartado {code} pelos últimos resultados")

    if status == 0:
        # somente valida o geral se os ultimos forem positivos
        status = lucro_resultado_geral(lc, media)
        if status == 1:
            print(f"Descartado {code} pelos lucros históricos negativos")

    return lc, media, status, ultimos_12m


def get_dre_details(code):
    dre = {}
    dre["lucro"], dre["media_lucro"], _, dre["lucro_12m"] = valida_empresa(code=code)

    return dre


def check_dre(code):
    dt = get_dre_details(code)
    return dt


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

        l, count, setores_an, empresas = [], 0, {}, set()
        for code, score in magic_result.items():
            details = check_dre(code)
            d = db.select_details(code)

            lucro = millify(details["media_lucro"])

            setor = d[0][0][0:12] if d[0][0] else "-"
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
            lpa = format_number(d[0][13], 0)
            div_ativo = format_number(d[0][14], 0)
            cagr_lucro = format_number(d[0][15], "-")
            cagr_receita = format_number(d[0][16], "-")

            if setor in setores_an:
                avg_pl = setores_an[setor]
            else:
                avg_pl = format_number(pl_setor(code), "-")
                setores_an[setor] = avg_pl

            l.append(
                [
                    count,
                    score,
                    code,
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
                    cagr_receita,
                    cagr_lucro,
                    div_pat,
                    div_ativo,
                    preco,
                    intriseco,
                    dist_min,
                ]
            )
            count += 1

            if len(empresas) == 30:
                break
            empresas.add(code[:4])

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
                    "CAGR Rec.%",
                    "CAGR Lc.%",
                    "Div/Pt",
                    "Div/EBIT.",
                    "Pr",
                    "Intr.",
                    "Dist.%",
                ],
                tablefmt="orgtbl",
            )
        )


if __name__ == "__main__":
    main()
