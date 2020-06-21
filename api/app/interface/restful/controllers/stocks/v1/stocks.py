import logging

from flask import request, jsonify
from flask_restplus import Namespace, Resource

import investpy as inv

api = Namespace("stocks", description="Stocks Codes")
logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class TechnicalQueryController(Resource):
    def post(self):
        return [{"type": "table", "rows": [], "columns": []}], 200


class TechnicalSearchController(Resource):
    def post(self):
        summary = inv.get_stocks_list(country="brazil")
        return summary, 200


api.add_resource(Health, "/", methods=["GET"])
api.add_resource(TechnicalQueryController, "/query", methods=["POST"])
api.add_resource(TechnicalSearchController, "/search", methods=["POST"])
