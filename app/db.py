import sqlite3


DATABASE = "database/fund.db"


def select():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute("""
        SELECT stockCode, setor, crescimentoCincoAnos, stockPrice, valorIntriseco, score, percentualDesconto, desconto, dividendos, "timestamp" 
        FROM fundamentus 
        WHERE coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY id DESC LIMIT 1) 
        AND crescimentoCincoAnos > 2
        AND ROE > 10
        AND desconto > 2
        ORDER by score DESC, percentualDesconto ASC, precoSobreLucro ASC, dividendos DESC, liquidezDoisMeses DESC
        LIMIT 20;
        """)
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

    cursor.executemany("""
        INSERT INTO 
            fundamentus
            (stockCode,
             patrimonioLiquido,
             liquidezCorrente,
             ROE,
             divSobrePatrimonio,
             crescimentoCincoAnos,
             precoSobreVP,
             precoSobreLucro,
             dividendos,
             stockPrice,
             PSR,
             precoSobreAtivo,
             precoSobreCapitalGiro,
             precoSobreEBIT,
             precoSobreAtivoCirculante,
             EVSobreEBIT,
             EVSobreEBITDA,
             margemEBIT,
             margemLiquida,
             ROIC,
             liquidezDoisMeses,
             timestamp,
             tipo,
             name,
             setor,
             subsetor,
             max52sem,
             volMed2M,
             valorMercado,
             valorFirma,
             nAcoes,
             lucroPorAcao,
             ValorPatrimonialPorAcao,
             margemBruta,
             EBITsobreAtivo,
             giroAtivos,
             ativo,
             lucroLiquido,
             receitaLiquida,
             disponibilidades,
             divBruta,
             divLiquida,
             valorIntriseco,
             score,
             desconto, 
             percentualDesconto,
             coletaUUID)
        VALUES
            (
            :stockCode,
            :patrimonioLiquido,
            :liquidezCorrente,
            :ROE,
            :divSobrePatrimonio,
            :crescimentoCincoAnos,
            :precoSobreVP,
            :precoSobreLucro,
            :dividendos,
            :stockPrice,
            :PSR,
            :precoSobreAtivo,
            :precoSobreCapitalGiro,
            :precoSobreEBIT,
            :precoSobreAtivoCirculante,
            :EVSobreEBIT,
            :EVSobreEBITDA,
            :margemEBIT,
            :margemLiquida,
            :ROIC,
            :liquidezDoisMeses,
            :timestamp,
            :tipo,
            :name,
            :setor,
            :subsetor,
            :max52sem,
            :volMed2M,
            :valorMercado,
            :valorFirma,
            :nAcoes,
            :lucroPorAcao,
            :ValorPatrimonialPorAcao,
            :margemBruta,
            :EBITsobreAtivo,
            :giroAtivos,
            :ativo,
            :lucroLiquido,
            :receitaLiquida,
            :disponibilidades,
            :divBruta,
            :divLiquida,
            :valorIntriseco,
            :score,
            :desconto,
            :percentualDesconto,
            :coletaUUID
            )""", data)
    connector.commit()

    cursor.close()
    connector.close()


def create_table():
    connector = sqlite3.connect(DATABASE)
    cursor = connector.cursor()

    cursor.execute('''CREATE TABLE fundamentus
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             stockCode TEXT,
             patrimonioLiquido NUMERIC,
             liquidezCorrente NUMERIC,
             ROE NUMERIC,
             divSobrePatrimonio NUMERIC,
             crescimentoCincoAnos NUMERIC,
             precoSobreVP NUMERIC,
             precoSobreLucro NUMERIC,
             dividendos NUMERIC,
             stockPrice NUMERIC,
             PSR NUMERIC,
             precoSobreAtivo NUMERIC,
             precoSobreCapitalGiro NUMERIC,
             precoSobreEBIT NUMERIC,
             precoSobreAtivoCirculante NUMERIC,
             EVSobreEBIT NUMERIC,
             EVSobreEBITDA NUMERIC,
             margemEBIT NUMERIC,
             margemLiquida NUMERIC,
             ROIC NUMERIC,
             liquidezDoisMeses NUMERIC,
             timestamp DATETIME,
             tipo TEXT,
             name TEXT,
             setor TEXT,
             subsetor TEXT,
             max52sem NUMERIC,
             volMed2M NUMERIC,
             valorMercado NUMERIC,
             valorFirma NUMERIC,
             nAcoes NUMERIC,
             lucroPorAcao NUMERIC,
             ValorPatrimonialPorAcao NUMERIC,
             margemBruta NUMERIC,
             EBITsobreAtivo NUMERIC,
             giroAtivos NUMERIC,
             ativo NUMERIC,
             lucroLiquido NUMERIC,
             receitaLiquida NUMERIC,
             disponibilidades NUMERIC,
             divBruta NUMERIC,
             divLiquida NUMERIC,
             valorIntriseco NUMERIC,
             score NUMERIC,
             desconto NUMERIC,
             percentualDesconto NUMERIC,
             coletaUUID TEXT);''')
    cursor.close()
    connector.close()
