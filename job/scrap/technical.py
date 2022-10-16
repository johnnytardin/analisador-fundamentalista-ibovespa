import logging
import time

import investpy as inv

from decouple import config


SCRAP_DATA_TECHNICAL = config('SCRAP_DATA_TECHNICAL', False)

logger = logging.getLogger(__name__)


def get_technical_indicators(code, interval="daily"):
    if not SCRAP_DATA_TECHNICAL:
        return {}

    time.sleep(1.5)
    try:
        data = inv.technical_indicators(
            code, country="brazil", product_type="stock", interval=interval
        )
    except ValueError as err:
        # investpy nao tem todos os tickers
        logger.warning(f"Falha coletando as dados técnicos. {err}")
        return {}
    except Exception as err:
        logger.warning(f"Falha coletando as dados técnicos. {err}")
        return {}

    indicators = {}
    for _, values in data.iterrows():
        indicators[values.technical_indicator] = [values.value, values.signal]

    return indicators
