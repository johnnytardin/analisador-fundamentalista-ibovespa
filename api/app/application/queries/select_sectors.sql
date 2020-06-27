select 
	data ->> 'setor' 
from financial
where coleta_id = (SELECT coleta_id FROM financial ORDER BY timestamp DESC LIMIT 1)
group by data ->> 'setor'
order by data ->> 'setor'
