import app.application.magic as magic


class MagicFormula:
    @staticmethod
    def ev_ebit_roic_query():
        rank = magic.rank("ev_ebit_roic", False, 30, None)
        return rank

    @staticmethod
    def pl_roe_query():
        rank = magic.rank("pl_roe", False, 30, None)
        return rank

    @staticmethod
    def columns():
        return magic.columns()
