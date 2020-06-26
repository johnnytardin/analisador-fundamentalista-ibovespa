import logging

from app.application import db

logger = logging.getLogger(__name__)


def financial_get_indicators(code):
    row = db.consulta_detalhes("financial", code)[0]
    return row
