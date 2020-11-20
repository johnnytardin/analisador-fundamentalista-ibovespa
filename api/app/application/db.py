import os

import psycopg2
from decouple import config


POSTGRES_HOST = config("POSTGRES_HOST", "")
POSTGRES_USER = config("POSTGRES_USER", "")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", "")
POSTGRES_DB = config("POSTGRES_DB", "")
DATABASE_URL = config("DATABASE_URL", None)


def get_conn():
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    else:
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
        "technical_per_stock": "queries/select_technical_per_stock.sql",
        "ev_ebit": "queries/select_ev_ebit.sql",
        "roic": "queries/select_roic.sql",
        "pl": "queries/select_pl.sql",
        "roe": "queries/select_roe.sql",
        "sectors": "queries/select_sectors.sql",
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


def sectors():
    conn = get_conn()
    cursor = conn.cursor()

    q = queries("sectors")
    cursor.execute(q)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # tuple to dict
    new_data = []
    for row in rows:
        new_data.append(row[0])

    return new_data
