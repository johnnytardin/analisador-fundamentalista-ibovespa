select 
stock_code
from fundamentus 
where coleta_id = (SELECT coleta_id FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and (details->>'liquidezMediaDiaria')::numeric > 200000
and (details->>'precoSobreLucro')::numeric > 0
and (details->>'ROE')::numeric > 0
and (details->>'liquidezCorrente')::numeric >= 0.75
and ((details->>'margemLiquida')::numeric >= 7 or (details->>'margemLiquida' is null))
and ((details->>'freeFloat')::numeric >= 15 or (details->>'freeFloat' is null))
order by details->>'precoSobreLucro' desc