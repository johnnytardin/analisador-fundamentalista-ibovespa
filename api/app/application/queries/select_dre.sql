select 
    data
from dre
where coleta_id = (SELECT coleta_id FROM dre ORDER BY timestamp DESC LIMIT 1)
