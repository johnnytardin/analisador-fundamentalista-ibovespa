import db
import reports.db as reportsdb

from numpy import percentile
from tabulate import tabulate


def get_result(tipo="todos"):
    if tipo == "financeiro":
        print("Score para o setor Financeiro")

        performance = db.select_roe()
        value = db.select_pl()
    else:
        print("Score para todos os setores")

        performance = db.select_roic()
        value = db.select_ev_ebit()

    p, v, magic_formula = {}, {}, {}
    count = 0
    for row in value:
        v[row[0]] = count
        count += 1

    count = 0
    for row in performance:
        p[row[0]] = count
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


def lucro_liquido(cnpj):
    rows = reportsdb.lucro_liquido(cnpj)

    l = {}
    for row in rows:
        tipo, ano, lucro = row
        if tipo == "PENÚLTIMO":
            a = int(ano)
            ano = a - 1
        l[int(ano)] = lucro
    return l


def get_dre_details(cnpj):
    dre = {}
    dre["lucro"] = lucro_liquido(cnpj)

    return dre


def check_dre(code):
    try:
        cnpj, _ = db.stock_code_cnpj(code)

        dt = get_dre_details(cnpj)

        status = 0
        if percentile([x for x in dt["lucro"].values()], 20) < 0:
            # se a empresa vem tendo prejuizo nos ultimos anos
            status = 1

    except TypeError:
        print(f"WARNING - CADASTRO - Falha coletando o CNPJ para {code}")
        return (-1, {})
    except IndexError:
        print(f"WARNING - CÁLCULO - Falha calculando o lucro para {code}")
        return (-1, {})

    return (status, dt)


def main():
    for t in ["financeiro", "todos"]:
        magic_result = get_result(t)

        l, count = [], 0
        for code, score in magic_result.items():
            status, details = check_dre(code)
            if status in [0, -1]:
                d = db.select_details(code)

                if status == -1:
                    # coloca um asterisco por algum erro no cálculo
                    code = f"{code}*"

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
                    ]
                )
                count += 1

                if count == 30:
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
                    "ROIC %",
                    "PL",
                    "ROE %",
                    "Dist.Min. %",
                    "Preço",
                    "Vlr.Intriseco",
                    "Desconto %",
                    "DY %",
                    "Cres.(5a) %",
                    "Div Br/ Patrim",
                    "Margem Liq. %",
                    "LPA",
                ],
                tablefmt="orgtbl",
            )
        )
        print("* Indicam algum erro para calcular.")


if __name__ == "__main__":
    main()
