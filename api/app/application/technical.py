import time
import json

import investpy as inv


class Technical:
    @staticmethod
    def get_indicators(stock, interval='weekly'):
        time.sleep(1.5)

        data = inv.technical_indicators(stock, country='brazil', product_type='stock', interval=interval).to_dict('records')
        return json.dumps(data)


    @staticmethod
    def get_moving_averages(stock, interval='weekly'):
        time.sleep(1.5)

        mov = inv.moving_averages(stock, country='brazil', product_type='stock', interval=interval).to_dict('records')
        return json.dumps(mov)
