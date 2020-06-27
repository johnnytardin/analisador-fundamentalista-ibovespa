import investpy as inv


def get_stocks_tickers(fiis=False, as_list=True):
    stocks = inv.get_stocks(country="brazil")

    if fiis:
        stocks = stocks[
            (stocks["isin"].str[-3:-1] == "00") | (stocks["isin"].str[-3:-1] == "01")
        ]
    else:
        stocks = stocks[
            (stocks["isin"].str[-3:-1] != "00") & (stocks["isin"].str[-3:-1] != "01")
        ]

    if as_list:
        stocks = stocks["symbol"].to_list()
        stocks.sort()

    return stocks
