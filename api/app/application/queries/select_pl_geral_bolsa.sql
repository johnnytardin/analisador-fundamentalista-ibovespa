select 
stock_code
from financial 
where coleta_id = (SELECT coleta_id FROM financial ORDER BY timestamp DESC LIMIT 1)
and (data->>'liquidezMediaDiaria')::numeric > 200000
and (data->>'precoSobreLucro')::numeric > 0
and (data->>'ROE')::numeric > 0
and (data->>'liquidezCorrente')::numeric >= 0.75
and ((data->>'margemLiquida')::numeric >= 7 or (data->>'margemLiquida' is null))
and ((data->>'freeFloat')::numeric >= 15 or (data->>'freeFloat' is null))
order by data->>'precoSobreLucro' desc
