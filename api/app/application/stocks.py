import logging

import investpy as inv


logger = logging.getLogger(__name__)


def get_stocks_tickers(fiis=False, as_list=True):
    stocks = inv.get_stocks(country="brazil")

    if fiis:
        stocks = stocks[stocks["isin"].str[-3:-1] == "00"]
    else:
        stocks = stocks[stocks["isin"].str[-3:-1] != "00"]

    if as_list:
        stocks = stocks["symbol"].to_list()
        stocks.sort()

    return stocks
