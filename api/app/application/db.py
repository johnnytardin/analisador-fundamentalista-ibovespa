import os
import json

import psycopg2


def get_conn():
    conn = psycopg2.connect(
        "dbname='analisador' user='analisador' host='postgres' password='analisador'"
    )
    return conn


def queries(tipo):
    files = {
        "dre": "queries/select_dre.sql",
        "technical": "queries/select_technical.sql",
        "average": "queries/select_average.sql",
        "financial": "queries/select_financial.sql",
        "dre_per_stock": "queries/select_dre_per_stock.sql",
        "technical_per_stock": "queries/select_technical_per_stock.sql",
        "average_per_stock": "queries/select_average_per_stock.sql",
        "financial_per_stock": "queries/select_financial_per_stock.sql",
        "pl_setor": "queries/select_pl_setor.sql",
        "pl_geral": "queries/select_pl_geral_bolsa.sql",
        "details": "queries/select_details.sql",
        "score": "queries/select_score.sql",
        "insert_fundamentus": "queries/insert_fundamentus.sql",
        "ev_ebit": "queries/select_ev_ebit.sql",
        "roic": "queries/select_roic.sql",
        "pl": "queries/select_pl.sql",
        "roe": "queries/select_roe.sql",
    }

    current_dir = os.path.abspath(os.path.dirname(__file__))
    query = os.path.join(current_dir, files[tipo])
    with open(query, "r") as e:
        return e.read()


def select_details(stockcode):
    conn = get_conn()
    cursor = conn.cursor()

    q = queries("details")
    cursor.execute(
        q, (stockcode,),
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def consulta_detalhes(tipo, stock=None):
    conn = get_conn()
    cursor = conn.cursor()

    if stock:
        tipo = f"{tipo}_per_stock"

    q = queries(tipo)
    cursor.execute(q, (stock,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # tuple to dict
    new_data = []
    for row in rows:
        new_data.append(row[0])

    return new_data
