import app.application.magic as magic


#TODO: gerar um outro endpoint com dados gerais da bolsa
#magic.pl_bolsa()


class MagicFormula:

    @staticmethod
    def ev_ebit_roic_query():
        rank = magic.rank("ev_ebit_roic", False, 10000, None)
        return rank

    @staticmethod
    def pl_roe_query():
        rank = magic.rank("pl_roe", False, 10000, None)
        return rank

    @staticmethod
    def columns():
        return magic.columns()


