select 
    data
from financial
where coleta_id = (SELECT coleta_id FROM financial ORDER BY timestamp DESC LIMIT 1)
and stock_code not like 'SAPR%'
and stock_code not like 'CPLE%'
and stock_code not like 'ELET%'
and stock_code not like 'CSMG%'