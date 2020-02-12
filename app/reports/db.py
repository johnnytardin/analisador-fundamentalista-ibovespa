import sqlite3


DATABASE = "rapina/.data/rapina.db"

def codigo_conta(tipo):
    t = {"lucro": 12, "dividendos": 18, "juros_capital_proprio": 17}
    return t[tipo]


def consulta_dre(nome, tipo):
    connector = sqlite3.connect(DATABASE)
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
