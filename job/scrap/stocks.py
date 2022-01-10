import os


def get_stocks_tickers(fiis=False):
    dir_path = os.path.dirname(os.path.abspath(__file__))

    if fiis:
        filename = f"{dir_path}/resources/fiis.txt"
    else:
        filename = f"{dir_path}/resources/stocks.txt"

    with open(filename) as file:
        lines = file.readlines()
        tickers = [line.rstrip() for line in lines]

    return tickers
