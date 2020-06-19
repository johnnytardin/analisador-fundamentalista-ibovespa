select 
    segmento,
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
    divSobrePatrimonio,
    margemLiquida,
    lucroPorAcao,
    divSobreEbit,
    CagrLucrosCincoAnos,
    CagrReceitasCincoAnos,
    Valorizacao12M,
    ValorizacaoMesAtual,
    ROA,
    ValorPatrimonialPorAcao
from fundamentus 
where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and stockCode = ?
