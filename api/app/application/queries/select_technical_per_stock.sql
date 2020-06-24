select 
    data
from indicators
where coleta_id = (SELECT coleta_id FROM indicators ORDER BY timestamp DESC LIMIT 1)
and stock_code = %s
