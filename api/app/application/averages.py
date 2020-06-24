import logging
import json

import app.application.db as db


logger = logging.getLogger(__name__)


def moving_averages(stock):
    averages = db.consulta_detalhes("average", stock)[0]

    avg = []
    for row in averages:
        avg.append([
            row["period"],
            row["sma_value"],
            row["sma_signal"],
            row["ema_value"],
            row["ema_signal"],
        ])
    return avg


def columns():
    return [
        {"text": "period", "type": "number"},
        {"text": "sma_value", "type": "number"},
        {"text": "sma_signal", "type": "text"},
        {"text": "ema_value", "type": "number"},
        {"text": "ema_signal", "type": "text"},
    ]
