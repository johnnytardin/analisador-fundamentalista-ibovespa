select 
    data
from dre
where coleta_id = (SELECT coleta_id FROM dre ORDER BY timestamp DESC LIMIT 1)
and stock_code not like 'SAPR%%'
and stock_code not like 'CPLE%%'
and stock_code not like 'ELET%%'
and stock_code not like 'CSMG%%'
