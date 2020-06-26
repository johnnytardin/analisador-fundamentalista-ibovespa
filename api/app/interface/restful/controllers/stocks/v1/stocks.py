import logging
from datetime import datetime 

from flask import request, jsonify
from flask_restplus import Namespace, Resource
import investpy as inv
import pendulum

from app.application import historical


api = Namespace("stocks", description="Stocks Codes")
logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class TechnicalQueryController(Resource):
    def post(self):
        return [{"type": "table", "rows": [], "columns": ["codes"]}], 200


class TechnicalSearchController(Resource):
    def post(self):
        summary = inv.get_stocks_list(country="brazil")
        return summary, 200


class HistoricalQueryController(Resource):
    def post(self):
        code = request.json.get("targets")[0].get("target")
        interval = request.json.get("scopedVars").get("Interval").get("value").title()

        range_time = request.json.get("range")
        range_from = pendulum.parse(range_time["from"]).format('DD/MM/YYYY')
        range_to = pendulum.parse(range_time["to"]).format('DD/MM/YYYY')

        ht_datapoints = historical.get_historical_data(code, range_from, range_to, interval)

        h = [{
            "target":"price",
            "datapoints": ht_datapoints
        }]

        return h, 200


api.add_resource(Health, "/", methods=["GET"])
api.add_resource(TechnicalQueryController, "/query", methods=["POST"])
api.add_resource(TechnicalSearchController, "/search", methods=["POST"])

api.add_resource(Health, "/historical/", methods=["GET"])
api.add_resource(HistoricalQueryController, "/historical/query", methods=["POST"])
api.add_resource(TechnicalSearchController, "/historical/search", methods=["POST"])
