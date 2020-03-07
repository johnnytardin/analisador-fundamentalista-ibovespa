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
