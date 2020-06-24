import app.application.magic as magic


def ev_ebit_roic_query():
    rank = magic.rank("ev_ebit_roic")
    return rank

def pl_roe_query():
    rank = magic.rank("pl_roe")
    return rank

def columns():
    return magic.columns()
