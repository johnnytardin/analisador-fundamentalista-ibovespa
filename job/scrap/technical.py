import time
import logging

import investpy as inv


logger = logging.getLogger(__name__)


def get_technical_indicators(code, interval="weekly"):
    time.sleep(1.5)

    data = inv.technical_indicators(
        code, country="brazil", product_type="stock", interval=interval
    )

    indicators = {}
    for _, values in data.iterrows():
        indicators[values.technical_indicator] = [values.value, values.signal]

    return indicators
