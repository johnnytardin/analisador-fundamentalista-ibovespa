import sqlite3


DATABASE = "database/fund.db"


def select():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """
        SELECT stockCode, setor, crescimentoCincoAnos, stockPrice, valorIntriseco, score, percentualDesconto, desconto, dividendos, "timestamp" 
        FROM fundamentus 
        WHERE coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1) 
        AND crescimentoCincoAnos > 2
        AND ROE > 10
        AND desconto > 0
        AND divSobrePatrimonio < 0.5
        AND precoSobreLucro <= 15 AND precoSobreLucro >= 0
        AND divSobreEbit <= 0.5
        AND dividendos > 4.5
        ORDER by score DESC, percentualDesconto ASC, precoSobreLucro ASC, dividendos DESC, liquidezMediaDiaria DESC
        LIMIT 20;
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def insert(data):
    try:
        create_table()
    except sqlite3.OperationalError:
        pass

    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.executemany(
        """
        INSERT INTO 
            fundamentus
            (
                stockCode,
                patrimonioLiquido,
                liquidezCorrente,
                ROE,
                divSobrePatrimonio,
                divSobreEbitda,
                divSobreEbit,
                PatrimonioSobreAtivos,
                CagrReceitasCincoAnos,
                CagrLucrosCincoAnos,
                crescimentoCincoAnos,
                precoSobreVP,
                precoSobreLucro,
                dividendos,
                stockPrice,
                PSR,
                precoSobreAtivo,
                precoSobreCapitalGiro,
                precoSobreEBIT,
                precoSobreEBITDA,
                precoSobreAtivoCirculante,
                EVSobreEBIT,
                EVSobreEBITDA,
                margemEBIT,
                margemEBITDA,
                margemLiquida,
                ROIC,
                ROA,
                liquidezMediaDiaria,
                "timestamp",
                setor,
                subsetor,
                segmento,
                max52sem,
                min52sem,
                PercDistanciaMin52sem,
                lucroPorAcao,
                ValorPatrimonialPorAcao,
                margemBruta,
                giroAtivos,
                lucroLiquido,
                valorIntriseco,
                score,
                percentualDesconto,
                coletaUUID
            )
        VALUES
            (
                :stockCode,
                :patrimonioLiquido,
                :liquidezCorrente,
                :ROE,
                :divSobrePatrimonio,
                :divSobreEbitda,
                :divSobreEbit,
                :PatrimonioSobreAtivos,
                :CagrReceitasCincoAnos,
                :CagrLucrosCincoAnos,
                :crescimentoCincoAnos,
                :precoSobreVP,
                :precoSobreLucro,
                :dividendos,
                :stockPrice,
                :PSR,
                :precoSobreAtivo,
                :precoSobreCapitalGiro,
                :precoSobreEBIT,
                :precoSobreEBITDA,
                :precoSobreAtivoCirculante,
                :EVSobreEBIT,
                :EVSobreEBITDA,
                :margemEBIT,
                :margemEBITDA,
                :margemLiquida,
                :ROIC,
                :ROA,
                :liquidezMediaDiaria,
                :timestamp,
                :setor,
                :subsetor,
                :segmento,
                :max52sem,
                :min52sem,
                :PercDistanciaMin52sem,
                :lucroPorAcao,
                :ValorPatrimonialPorAcao,
                :margemBruta,
                :giroAtivos,
                :lucroLiquido,
                :valorIntriseco,
                :score,
                :percentualDesconto,
                :coletaUUID
            )""",
        data,
    )
    connector.commit()

    cursor.close()
    connector.close()


def select_ev_ebit():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """
        select 
        stockCode
        from fundamentus 
        where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
        and liquidezMediaDiaria > 200000
        and segmento != 'Bancos'
        and (divSobreEbit <= 2 or divSobrePatrimonio <= 2)
        and EVSobreEBIT >= 0
        --and ROIC >= 0
        and precoSobreLucro > 0
        order by EVSobreEBIT desc 
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def select_roic():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """
        select 
        stockCode
        from fundamentus 
        where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
        and liquidezMediaDiaria > 200000
        and segmento != 'Bancos'
        and (divSobreEbit <= 2 or divSobrePatrimonio <= 2)
        and EVSobreEBIT >= 0
        --and ROIC >= 0
        and precoSobreLucro > 0
        order by ROIC asc 
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def select_pl():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """
        select 
        stockCode
        from fundamentus 
        where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
        and liquidezMediaDiaria > 200000
        and segmento = 'Bancos'
        and precoSobreLucro > 0
        and ROE > 0
        order by precoSobreLucro desc 
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def select_roe():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """
        select 
        stockCode
        from fundamentus 
        where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
        and liquidezMediaDiaria > 200000
        and segmento = 'Bancos'
        and precoSobreLucro > 0
        and ROE > 0
        order by ROE asc
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def select_details(stockcode):
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """
        select 
            subsetor,
            precoSobreVP,
            EVSobreEBIT, 
            ROIC, 
            precoSobreLucro, 
            ROE, 
            PercDistanciaMin52sem, 
            stockPrice, 
            valorIntriseco, 
            PercentualDesconto, 
            dividendos,
            crescimentoCincoAnos,
            divSobrePatrimonio,
            margemLiquida,
            lucroPorAcao,
            divSobreEbit
        from fundamentus 
        where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
        and stockCode = ?
        """,
        (stockcode,),
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def pl_setor(stockcode):
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """
        select 
            PrecoSobreLucro
        from fundamentus 
        where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
        and setor = (select setor from fundamentus where stockCode = ? LIMIT 1)
        and precoSobreLucro > 0
        """,
        (stockcode,),
    )
    rows = cursor.fetchall()

    cursor.close()
    connector.close()
    return rows


def create_table():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute(
        """CREATE TABLE fundamentus
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             stockCode TEXT,
             patrimonioLiquido NUMERIC,
             liquidezCorrente NUMERIC,
             ROE NUMERIC,
             divSobrePatrimonio NUMERIC,
             divSobreEbitda NUMERIC,
             divSobreEbit NUMERIC,
             PatrimonioSobreAtivos NUMERIC,
             CagrReceitasCincoAnos NUMERIC,
             CagrLucrosCincoAnos NUMERIC,
             crescimentoCincoAnos NUMERIC,
             precoSobreVP NUMERIC,
             precoSobreLucro NUMERIC,
             dividendos NUMERIC,
             stockPrice NUMERIC,
             PSR NUMERIC,
             precoSobreAtivo NUMERIC,
             precoSobreCapitalGiro NUMERIC,
             precoSobreEBIT NUMERIC,
             precoSobreEBITDA NUMERIC,
             precoSobreAtivoCirculante NUMERIC,
             EVSobreEBIT NUMERIC,
             EVSobreEBITDA NUMERIC,
             margemEBIT NUMERIC,
             margemEBITDA NUMERIC,
             margemLiquida NUMERIC,
             ROIC NUMERIC,
             ROA NUMERIC,
             liquidezMediaDiaria NUMERIC,
             timestamp DATETIME,
             setor TEXT,
             subsetor TEXT,
             segmento TEXT,
             max52sem NUMERIC,
             min52sem NUMERIC,
             PercDistanciaMin52sem NUMERIC,
             lucroPorAcao NUMERIC,
             ValorPatrimonialPorAcao NUMERIC,
             margemBruta NUMERIC,
             giroAtivos NUMERIC,
             lucroLiquido NUMERIC,
             valorIntriseco NUMERIC,
             score NUMERIC,
             percentualDesconto NUMERIC,
             coletaUUID TEXT);"""
    )
    cursor.close()
    connector.close()


def stock_code_cnpj(code):
    connector = sqlite3.connect(DATABASE)
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
