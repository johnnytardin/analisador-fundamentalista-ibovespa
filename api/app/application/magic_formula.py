import app.application.magic as magic


def ev_ebit_roic_query(payload):
    rank = magic.rank("ev_ebit_roic", payload)
    return rank


def pl_roe_query(payload):
    rank = magic.rank("pl_roe", payload)
    return rank


def columns():
    return magic.columns()
