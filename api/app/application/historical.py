import time
import logging

import investpy as inv


logger = logging.getLogger(__name__)


def get_historical_data(code, from_date, to_date, interval):
    time.sleep(1.5)

    if interval not in ["Daily", "Weekly", "Monthly"]:
        interval = "Daily"

    data = inv.get_stock_historical_data(
        code, "brazil", from_date, to_date, interval=interval
    )

    h = []
    for index, values in data.iterrows():
        h.append(
            [values.Close, index.timestamp() * 1000]
        )
    return h
