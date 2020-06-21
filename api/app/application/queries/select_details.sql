select 
    details->>'segmento',
    details->>'precoSobreVP',
    details->>'EVSobreEBIT', 
    details->>'ROIC', 
    details->>'precoSobreLucro', 
    details->>'ROE', 
    details->>'PercDistanciaMin52sem', 
    details->>'stockPrice', 
    details->>'valorIntriseco', 
    details->>'PercentualDesconto', 
    details->>'dividendos',
    details->>'divSobrePatrimonio',
    details->>'margemLiquida',
    details->>'lucroPorAcao',
    details->>'divSobreEbit',
    details->>'CagrLucrosCincoAnos',
    details->>'CagrReceitasCincoAnos',
    details->>'Valorizacao12M',
    details->>'ValorizacaoMesAtual',
    details->>'ROA',
    details->>'ValorPatrimonialPorAcao'
from fundamentus 
where coleta_id = (SELECT coleta_id FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and stock_code = %s