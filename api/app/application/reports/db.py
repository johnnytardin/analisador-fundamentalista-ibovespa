import sqlite3


DATABASE_REPORTS = "../rapina/.data/rapina.db"
DATABASE_HST = "database/fund.db"


def codigo_conta(tipo):
    t = {"lucro": 12, "dividendos": 18, "juros_capital_proprio": 17}
    return t[tipo]


def consulta_dre(nome, tipo):
    connector = sqlite3.connect(DATABASE_REPORTS)
    cursor = connector.cursor()
    code = codigo_conta(tipo)

    cursor.execute(
        """
            SELECT
                ORDEM_EXERC,
                strftime("%Y", (DATETIME(ROUND(DT_REFER), 'unixepoch'))) AS DT_REFER,
                VL_CONTA,
                ESCALA_MOEDA
            FROM
                dfp
            WHERE
                CNPJ_CIA = ?
                AND CODE = ?
                AND (ORDEM_EXERC LIKE "_LTIMO"
                    OR (
                        ORDEM_EXERC LIKE "PEN_LTIMO"
                        AND DT_REFER = (SELECT MIN(DT_REFER) FROM dfp WHERE CNPJ_CIA = ?)
                    )
                )
            ORDER BY
                DT_REFER
        """,
        (nome, code, nome,),
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def stock_code_cnpj(code):
    connector = sqlite3.connect(DATABASE_HST)
    cursor = connector.cursor()

    cursor.execute(
        """
        select cnpj, nome from cnpj_code where stock_code = ?
        """,
        (code,),
    )
    row = cursor.fetchone()

    if not row:
        cursor.execute(
            """
            select cnpj, nome from cnpj_code where stock_code like ?
            """,
            (f"%{code}%",),
        )
        row = cursor.fetchone()

    cursor.close()
    connector.close()
    return row
