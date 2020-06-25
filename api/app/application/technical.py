from datetime import datetime
import time
import logging
import json

import app.application.db as db
import app.application.lucros as lucros

from alpha_vantage.techindicators import TechIndicators
from decouple import config
import investpy as inv


logger = logging.getLogger(__name__)


API_KEY_ALPHA_VALUE = config("API_KEY_ALPHA_VALUE")


def indicators_stock(indicator, code, interval, range_from, range_to):
    ti = TechIndicators(key=API_KEY_ALPHA_VALUE, output_format='pandas')
    data, _ = ti.get_rsi(symbol=f'{code}.SAO', interval=interval, time_period=14)
    data = data.loc[range_from:range_to]

    serie = {"target": "rsi_14"}
    result = []
    for index, row in data.iterrows():
        unix_timestamp = index.timestamp() * 1000
        result.append([row.RSI, unix_timestamp])
    serie["datapoints"] = result

    return [serie]


#TODO: desenvolver uma forma resumida?
def get_indicators(code, interval='weekly'):
    time.sleep(1.5)

    data = inv.technical_indicators(code, country='code', product_type='stock', interval=interval).to_dict('records')

    counters = {}
    for i in data:
        signal = i["signal"]
        if signal in counters:
            counters[signal] += 1
        else:
            counters[signal] = 1

    return counters


def get_moving_averages(stock, interval='weekly'):
    time.sleep(1.5)

    mov = inv.moving_averages(stock, country='brazil', product_type='stock', interval=interval).to_dict('records')

    counters = {}
    for i in mov:
        signal = i["ema_signal"]
        if signal in counters:
            counters[signal] += 1
        else:
            counters[signal] = 1
    return counters