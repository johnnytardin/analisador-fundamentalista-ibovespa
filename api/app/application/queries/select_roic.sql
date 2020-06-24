select 
stock_code
from financial 
where coleta_id = (SELECT coleta_id FROM financial ORDER BY timestamp DESC LIMIT 1)
and (data->>'liquidezMediaDiaria')::numeric > 200000
and (data->>'EVSobreEBIT')::numeric >= 0
and (data->>'ROIC')::numeric >= 0
and (data->>'liquidezCorrente')::numeric >= 0.75
and (((data->>'divSobreEbit')::numeric <= 2 or (data->>'divSobreEbit') is null) or ((data->>'divSobrePatrimonio')::numeric <= 2 or (data->>'divSobrePatrimonio' is null)))
and ((data->>'CagrLucrosCincoAnos')::numeric > 0.5 or (data->>'CagrLucrosCincoAnos' is null))
and ((data->>'precoSobreLucro')::numeric > 0 or (data->>'precoSobreLucro' is null))
and ((data->>'margemLiquida')::numeric >= 7 or (data->>'margemLiquida' is null))
and ((data->>'freeFloat')::numeric >= 15 or (data->>'freeFloat' is null))
order by (data->>'ROIC')::numeric asc