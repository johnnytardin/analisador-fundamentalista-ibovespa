select 
    PrecoSobreLucro
from fundamentus 
where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and setor = (select setor from fundamentus where stockCode = ? LIMIT 1)
and precoSobreLucro > 0
