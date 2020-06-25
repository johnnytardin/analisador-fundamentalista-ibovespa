import logging

import pendulum
from flask import request, jsonify
from flask_restplus import Namespace, Resource

from app.application.technical import indicators_stock


api = Namespace("technical", description="Technical Informations")
logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200

class TechnicalSearchController(Resource):
    def post(self):
        return {"target": ""}, 200

class TechnicalAnnotationsController(Resource):
    def post(self):
        return [], 200

class TechnicalQueryController(Resource):
    def post(self):
        code = request.json.get("targets")[0].get("target")
        indicator = request.json.get("targets")[0].get("data").get("indicator")
        interval = request.json.get("scopedVars").get("Interval").get("value")

        range_time = request.json.get("range")
        range_from = pendulum.parse(range_time["from"])
        range_to = pendulum.parse(range_time["to"])

        summary = indicators_stock(indicator, code, interval, range_from, range_to)
        return summary, 200

api.add_resource(Health, "/", methods=["GET"])
api.add_resource(TechnicalQueryController, "/query", methods=["POST"])
api.add_resource(TechnicalSearchController, "/search", methods=["POST"])
api.add_resource(TechnicalAnnotationsController, "/annotations", methods=["POST"])
