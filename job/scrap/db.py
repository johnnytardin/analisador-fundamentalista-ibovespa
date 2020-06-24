import os

import json
import psycopg2


def get_conn():
    conn = psycopg2.connect(
        "dbname='analisador' user='analisador' host='localhost' password='analisador'"
    )
    return conn


def queries(tipo):
    files = {
        "create": "queries/create_tables.sql",
        "insert": "queries/insert_data.sql",
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


def create_table():
    conn = get_conn()
    cursor = conn.cursor()

    qf = queries("create")
    cursor.execute(qf)
    conn.commit()

    cursor.close()
    conn.close()
