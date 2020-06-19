select 
stockCode
from fundamentus 
where coletaUUID = (SELECT coletaUUID FROM fundamentus ORDER BY timestamp DESC LIMIT 1)
and liquidezMediaDiaria > 200000
and valorMercado <= 4000000000
and precoSobreLucro > 0
and ROA > 0
and liquidezCorrente >= 0.75
and (margemLiquida >= 7 or margemLiquida is null)
and (freeFloat >= 15 or freeFloat is null)
order by ROE asc
