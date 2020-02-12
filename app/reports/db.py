import sqlite3


DATABASE = "rapina/.data/rapina.db"


def lucro_liquido(nome):
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """
            SELECT
                ORDEM_EXERC,
                strftime("%Y", (DATETIME(ROUND(DT_REFER), 'unixepoch'))) AS DT_REFER,
                VL_CONTA
            FROM
                dfp
            WHERE
                CNPJ_CIA = ?
                AND CODE = '12'
                AND (ORDEM_EXERC LIKE "_LTIMO"
                    OR (
                        ORDEM_EXERC LIKE "PEN_LTIMO"
                        AND DT_REFER = (SELECT MIN(DT_REFER) FROM dfp WHERE CNPJ_CIA = ?)
                    )
                )
            ORDER BY
                DT_REFER
        """,
        (nome, nome,),
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows
