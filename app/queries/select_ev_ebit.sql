select 
stockCode
from fundamentus 
where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and liquidezMediaDiaria > 200000
and EVSobreEBIT >= 0
and ROIC >= 0
and ((divSobreEbit <= 2 or divSobreEbit is null) or (divSobrePatrimonio <= 2 or divSobrePatrimonio))
and (CagrLucrosCincoAnos > 0.5 or CagrLucrosCincoAnos is null)
and (precoSobreLucro > 0 or precoSobreLucro is null)
and (margemLiquida >= 7 or margemLiquida is null)
and (freeFloat >= 15 or freeFloat is null)
order by EVSobreEBIT desc 
