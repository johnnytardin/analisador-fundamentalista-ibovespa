select 
stockCode
from fundamentus 
where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and liquidezMediaDiaria > 200000
and precoSobreLucro > 0
and ROE > 0
and (margemLiquida >= 7 or margemLiquida is null)
order by precoSobreLucro desc 
