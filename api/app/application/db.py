import os
import json

import psycopg2
from decouple import config


POSTGRES_HOST = config("POSTGRES_HOST")
POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
POSTGRES_DB = config("POSTGRES_DB")


def get_conn():
    conn = psycopg2.connect(
        f"dbname={POSTGRES_DB} user={POSTGRES_USER} host={POSTGRES_HOST} password={POSTGRES_PASSWORD}"
    )
    return conn


def queries(tipo):
    files = {
        "dre": "queries/select_dre.sql",
        "financial": "queries/select_financial.sql",
        "dre_per_stock": "queries/select_dre_per_stock.sql",
        "financial_per_stock": "queries/select_financial_per_stock.sql",
        "ev_ebit": "queries/select_ev_ebit.sql",
        "roic": "queries/select_roic.sql",
        "pl": "queries/select_pl.sql",
        "roe": "queries/select_roe.sql",
    }

    current_dir = os.path.abspath(os.path.dirname(__file__))
    query = os.path.join(current_dir, files[tipo])
    with open(query, "r") as e:
        return e.read()


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
