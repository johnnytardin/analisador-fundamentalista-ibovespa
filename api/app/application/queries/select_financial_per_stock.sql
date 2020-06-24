select 
    data
from financial
where coleta_id = (SELECT coleta_id FROM financial ORDER BY timestamp DESC LIMIT 1)
and stock_code = %s
