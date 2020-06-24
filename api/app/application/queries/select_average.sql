select 
    data
from averages
where coleta_id = (SELECT coleta_id FROM averages ORDER BY timestamp DESC LIMIT 1)
