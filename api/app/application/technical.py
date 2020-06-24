import logging
import json

import app.application.db as db


logger = logging.getLogger(__name__)


def indicators(stock):
    indicators = db.consulta_detalhes("technical", stock)[0]

    i = []
    for row in indicators:
        i.append([row["technical_indicator"], row["value"], row["signal"]])

    return i


def columns():
    return [
        {"text": "technical_indicator", "type": "string"},
        {"text": "value", "type": "number"},
        {"text": "signal", "type": "string"},
    ]
