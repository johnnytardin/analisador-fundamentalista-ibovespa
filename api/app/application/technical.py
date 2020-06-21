import logging
import json

import app.application.db as db


logger = logging.getLogger(__name__)


def technical_indicators(stock):
    rows = db.consulta_detalhes(stock, "tecnicos")

    indicadores = {}
    for row in rows:
        indicadores[row["technical_indicator"]] = {
            "value": row["value"],
            "signal": row["signal"],
        }
    return indicadores


def moving_averages(stock, interval="weekly"):
    medias = db.consulta_detalhes(stock, "medias")
    return medias


def indicators(stock):
    t = technical_indicators(stock)
    m = moving_averages(stock)

    return [t["RSI(14)"]["value"]] 


def columns():
    return [
        {"text": "RSI", "type": "number"},
    ]
