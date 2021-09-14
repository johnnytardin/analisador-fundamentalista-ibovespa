import logging
import time

import investpy as inv

logger = logging.getLogger(__name__)


def get_technical_indicators(code, interval="daily"):
    time.sleep(1.5)

    try:
        data = inv.technical_indicators(
            code, country="brazil", product_type="stock", interval=interval
        )
    except ValueError:
        # investpy nao tem todos os tickers
        return {}

    indicators = {}
    for _, values in data.iterrows():
        indicators[values.technical_indicator] = [values.value, values.signal]

    return indicators
