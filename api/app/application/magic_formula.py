import app.application.magic as magic


def ev_ebit_roic_query(promocao):
    rank = magic.rank("ev_ebit_roic", promocao)
    return rank


def pl_roe_query(promocao):
    rank = magic.rank("pl_roe", promocao)
    return rank


def columns():
    return magic.columns()
