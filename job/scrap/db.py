import sqlite3
DATABASE = "teste"


import os

import json
import psycopg2


def get_conn():
    conn = psycopg2.connect("dbname='analisador' user='analisador' host='localhost' password='analisador'")
    return conn


def queries(tipo):
    files = {
        "create_fundamentus": "queries/create_table_fundamentus.sql",
        "insert_fundamentus": "queries/insert_fundamentus.sql",
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


def insert_fundamentus(stock, coleta_id, timestamp, data):
    create_table()

    conn = get_conn()
    cursor = conn.cursor()

    q = queries("insert_fundamentus")
    cursor.execute(q, (stock, coleta_id, timestamp, json.dumps(data)))
    conn.commit()

    cursor.close()
    conn.close()


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
    conn = get_conn()
    cursor = conn.cursor()

    qf = queries("create_fundamentus")
    cursor.execute(qf)
    conn.commit()

    cursor.close()
    conn.close()


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
