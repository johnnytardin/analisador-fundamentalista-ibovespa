import json
import os

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
        "create": "queries/create_tables.sql",
        "insert": "queries/insert_data.sql",
        "delete": "queries/delete_data.sql",
    }

    current_dir = os.path.abspath(os.path.dirname(__file__))
    query = os.path.join(current_dir, files[tipo])
    with open(query, "r") as e:
        return e.read()


def insert_data(table, code, coleta_id, timestamp, data):
    create_table()

    conn = get_conn()
    cursor = conn.cursor()

    q = queries("insert").format(table)

    cursor.execute(q, (code, coleta_id, timestamp, json.dumps(data)))
    conn.commit()

    cursor.close()
    conn.close()


def delete_data():
    conn = get_conn()
    cursor = conn.cursor()

    qf = queries("delete")
    cursor.execute(qf)
    conn.commit()

    cursor.close()
    conn.close()


def create_table():
    conn = get_conn()
    cursor = conn.cursor()

    qf = queries("create")
    cursor.execute(qf)
    conn.commit()

    cursor.close()
    conn.close()
