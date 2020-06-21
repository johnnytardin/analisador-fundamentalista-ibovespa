--#TODO: acertar a comparação dos textos abaixo
select
	details->'PrecoSobreLucro'
from fundamentus 
where coleta_id = (SELECT coleta_id FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and (details->>'setor')::text = (select details->'setor' from fundamentus where stock_code = 'ABCB4' LIMIT 1)::text
and (details->>'precoSobreLucro')::numeric > 0
