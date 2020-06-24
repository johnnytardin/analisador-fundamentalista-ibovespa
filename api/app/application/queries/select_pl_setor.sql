--#TODO: acertar a comparação dos textos abaixo
select
	data->'PrecoSobreLucro'
from financial 
where coleta_id = (SELECT coleta_id FROM financial ORDER BY timestamp DESC LIMIT 1)
and (data->>'setor')::text = (select data->'setor' from financial where stock_code = 'ABCB4' LIMIT 1)::text
and (data->>'precoSobreLucro')::numeric > 0
