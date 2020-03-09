import sqlite3
import os

DATABASE = "database/fund.db"


def queries(tipo):
    files = {
        "detalhes_stock": "queries/select_detalhes_stock.sql",
        "create_detalhamento_historico": "queries/create_table_detalhamento_historico.sql",
        "create_fundamentus": "queries/create_table_fundamentus.sql",
        "pl_setor": "queries/select_pl_setor.sql",
        "pl_geral": "queries/select_pl_geral_bolsa.sql",
        "details": "queries/select_details.sql",
        "score": "queries/select_score.sql",
        "insert_fundamentus": "queries/insert_fundamentus.sql",
        "insert_dre": "queries/insert_dre.sql",
        "update_dre": "queries/update_dre.sql",
        "ev_ebit": "queries/select_ev_ebit.sql",
        "ev_ebit_small_caps": "queries/select_ev_ebit_small_caps.sql",
        "roic": "queries/select_roic.sql",
        "roic_small_caps": "queries/select_roic_small_caps.sql",
        "pl": "queries/select_pl.sql",
        "pl_small_caps": "queries/select_pl_small_caps.sql",
        "roe": "queries/select_roe.sql",
        "roe_small_caps": "queries/select_roe_small_caps.sql",
    }

    current_dir = os.path.abspath(os.path.dirname(__file__))
    query = os.path.join(current_dir, files[tipo])
    with open(query, "r") as e:
        return e.read()


def select():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    q = queries("score")
    cursor.execute(q)
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def insert_fundamentus(data):
    create_table()

    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    q = queries("insert_fundamentus")
    cursor.executemany(q, data)
    connector.commit()

    cursor.close()
    connector.close()


def insert_dre(data):
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    try:
        q = queries("insert_dre")
        cursor.executemany(
            q, data,
        )
    except sqlite3.IntegrityError:
        q = queries("update_dre")
        cursor.executemany(
            q, data,
        )
    except Exception as err:
        print(f"Falha inserindo dados históricos no banco de dados. Causa: {err}")
    finally:
        connector.commit()

    cursor.close()
    connector.close()


def select_rank_magic_formula(estrategia, small_cap=False):
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    # arqui está o chaveamento dos tipos para as queries
    if not small_cap:
        r1_tipo = "ev_ebit"
        r2_tipo = "roic"
        if estrategia == "pl_roe":
            r1_tipo = "pl"
            r2_tipo = "roe"
    else:
        r1_tipo = "ev_ebit_small_caps"
        r2_tipo = "roic_small_caps"
        if estrategia == "pl_roe":
            r1_tipo = "pl_small_caps"
            r2_tipo = "roe_small_caps"

    qr1 = queries(r1_tipo)
    qr2 = queries(r2_tipo)

    cursor.execute(qr1)
    rank_1 = cursor.fetchall()

    cursor.execute(qr2)
    rank_2 = cursor.fetchall()

    cursor.close()
    connector.close()
    return (rank_1, rank_2)


def select_details(stockcode):
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    q = queries("details")
    cursor.execute(
        q, (stockcode,),
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def pl_setor(stockcode):
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    q = queries("pl_setor")
    cursor.execute(
        q, (stockcode,),
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def pl_geral():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    q = queries("pl_geral")
    cursor.execute(q)
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def create_table():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    qf = queries("create_fundamentus")
    cursor.execute(qf)

    qdh = queries("create_detalhamento_historico")
    cursor.execute(qdh)

    cursor.close()
    connector.close()


def consulta_detalhes_periodo(stock, tipo):
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    # TODO: add os demais
    if tipo == "lucro":
        t = "Lucro Líquido - (R$)"

    q = queries("detalhes_stock")
    cursor.execute(
        q, (stock, t,),
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows
