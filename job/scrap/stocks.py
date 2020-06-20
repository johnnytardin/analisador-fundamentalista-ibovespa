import investpy as inv


def stocks_codes():
    return inv.get_stocks_list(country="brazil")
