import logging

import pendulum
from flask import request, jsonify
from flask_restplus import Namespace, Resource

from app.application import technical


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


class IndicatorsQueryController(Resource):
    def post(self):
        code = request.json.get("targets")[0].get("target")
        interval = request.json.get("scopedVars").get("Interval").get("value")

        summary = technical.get_technical_indicators(code, interval)
        columns = technical.columns_technical_indicators()

        return [{"type": "table", "rows": summary, "columns": columns}], 200


class MovingAveragesQueryController(Resource):
    def post(self):
        code = request.json.get("targets")[0].get("target")
        interval = request.json.get("scopedVars").get("Interval").get("value")

        summary = technical.get_moving_averages(code, interval)
        columns = technical.columns_moving_averages()

        return [{"type": "table", "rows": summary, "columns": columns}], 200


api.add_resource(Health, "/indicators/", methods=["GET"])
api.add_resource(IndicatorsQueryController, "/indicators/query", methods=["POST"])
api.add_resource(TechnicalSearchController, "/indicators/search", methods=["POST"])
api.add_resource(
    TechnicalAnnotationsController, "/indicators/annotations", methods=["POST"]
)

api.add_resource(Health, "/movingaverages/", methods=["GET"])
api.add_resource(
    MovingAveragesQueryController, "/movingaverages/query", methods=["POST"]
)
api.add_resource(TechnicalSearchController, "/movingaverages/search", methods=["POST"])
api.add_resource(
    TechnicalAnnotationsController, "/movingaverages/annotations", methods=["POST"]
)
