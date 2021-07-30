import logging
import time

import investpy as inv

logger = logging.getLogger(__name__)


def get_technical_indicators(code, interval="weekly"):
    time.sleep(1.5)

    data = inv.technical_indicators(
        code, country="brazil", product_type="stock", interval=interval
    )

    indicators_list = []
    for _, values in data.iterrows():
        indicators_list.append(
            [values.technical_indicator, values.value, values.signal]
        )

    return indicators_list


def columns_technical_indicators():
    return [
        {"text": "TECHNICAL INDICATOR", "type": "string"},
        {"text": "VALUE", "type": "number"},
        {"text": "SIGNAL", "type": "string"},
    ]


def get_moving_averages(stock, interval="weekly"):
    time.sleep(1.5)

    mov = inv.moving_averages(
        stock, country="brazil", product_type="stock", interval=interval
    )

    moving_list = []
    for _, values in mov.iterrows():
        moving_list.append(
            [
                values.period,
                values.sma_value,
                values.sma_signal,
                values.ema_value,
                values.ema_signal,
            ]
        )

    return moving_list


def columns_moving_averages():
    return [
        {"text": "PERIOD", "type": "number"},
        {"text": "SMA VALUE", "type": "number"},
        {"text": "SMA SIGNAL", "type": "string"},
        {"text": "EMA VALUE", "type": "number"},
        {"text": "EMA SIGNAL", "type": "string"},
    ]
