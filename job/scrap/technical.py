import time

import investpy as inv


def get_indicators(stock, interval="weekly"):
    time.sleep(1.5)

    data = inv.technical_indicators(
        stock, country="brazil", product_type="stock", interval=interval
    ).to_dict("records")

    return data


def get_moving_averages(stock, interval="weekly"):
    time.sleep(1.5)

    mov = inv.moving_averages(
        stock, country="brazil", product_type="stock", interval=interval
    ).to_dict("records")

    return mov
