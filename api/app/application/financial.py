from app.application import db


def financial_get_indicators(code):
    row = db.consulta_detalhes("financial", code)[0]
    return row
