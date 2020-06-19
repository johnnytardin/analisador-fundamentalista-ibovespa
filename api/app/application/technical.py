import time

import investpy as inv


class Technical:
    @staticmethod
    def get_indicators(stock, interval='weekly'):
        time.sleep(1.5)

        data = inv.technical_indicators(stock, country='brazil', product_type='stock', interval=interval).to_dict('records')

        counters = {}
        for i in data:
            signal = i["signal"]
            if signal in counters:
                counters[signal] += 1
            else:
                counters[signal] = 1

        return counters


    @staticmethod
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
