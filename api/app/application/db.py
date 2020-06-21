import sqlite3

DATABASE = "app/database/fund.db"

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
        "detalhes_stock": "queries/select_detalhes_stock.sql",
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


def select():
    conn = get_conn()
    cursor = conn.cursor()

    q = queries("score")
    cursor.execute(q)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def select_rank_magic_formula(estrategia):
    conn = get_conn()
    cursor = conn.cursor()

    # arqui está o chaveamento dos tipos para as queries
    r1_tipo = "ev_ebit"
    r2_tipo = "roic"
    if estrategia == "pl_roe":
        r1_tipo = "pl"
        r2_tipo = "roe"

    qr1 = queries(r1_tipo)
    qr2 = queries(r2_tipo)

    cursor.execute(qr1)
    rank_1 = cursor.fetchall()

    cursor.execute(qr2)
    rank_2 = cursor.fetchall()

    cursor.close()
    conn.close()
    return (rank_1, rank_2)


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


def pl_setor(stockcode):
    conn = get_conn()
    cursor = conn.cursor()

    q = queries("pl_setor")
    cursor.execute(
        q, (stockcode,),
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def pl_geral():
    conn = get_conn()
    cursor = conn.cursor()

    q = queries("pl_geral")
    cursor.execute(q)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows


def consulta_detalhes(stock, tipo="dre"):
    conn = get_conn()
    cursor = conn.cursor()

    q = queries("detalhes_stock")

    cursor.execute(q, (stock,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows[0][0][tipo]
