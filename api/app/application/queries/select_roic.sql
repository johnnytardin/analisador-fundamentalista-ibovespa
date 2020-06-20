select 
stockCode
from fundamentus 
where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and liquidezMediaDiaria > 200000
and ((divSobreEbit <= 2 or divSobreEbit is null) or (divSobrePatrimonio <= 2 or divSobrePatrimonio))
and EVSobreEBIT >= 0
and ROIC >= 0
and liquidezCorrente >= 0.75
and (CagrLucrosCincoAnos > 0.5 or CagrLucrosCincoAnos is null)
and (precoSobreLucro > 0 or precoSobreLucro is null)
and (margemLiquida >= 7 or margemLiquida is null)
and (freeFloat >= 15 or freeFloat is null)
order by ROIC asc 


select 
stock_code
from fundamentus 
where coleta_id = (SELECT coleta_id FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and (details->>'liquidezMediaDiaria')::numeric > 200000
and (details->>'EVSobreEBIT')::numeric >= 0
and (details->>'ROIC')::numeric >= 0
and (details->>'liquidezCorrente')::numeric >= 0.75
and (((details->>'divSobreEbit')::numeric <= 2 or (details->>'divSobreEbit') is null) or ((details->>'divSobrePatrimonio')::numeric <= 2 or (details->>'divSobrePatrimonio' is null)))
and ((details->>'CagrLucrosCincoAnos')::numeric > 0.5 or (details->>'CagrLucrosCincoAnos' is null))
and ((details->>'precoSobreLucro')::numeric > 0 or (details->>'precoSobreLucro' is null))
and ((details->>'margemLiquida')::numeric >= 7 or (details->>'margemLiquida' is null))
and ((details->>'freeFloat')::numeric >= 15 or (details->>'freeFloat' is null))
order by details->>'ROIC' asc