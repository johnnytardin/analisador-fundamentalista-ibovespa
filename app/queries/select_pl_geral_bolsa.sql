select 
    PrecoSobreLucro
from fundamentus 
where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and precoSobreLucro > 0
