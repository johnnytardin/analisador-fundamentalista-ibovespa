select periodo, valor 
from detalhamento_historico
where stock = ?
and tipo like ?
order by periodo