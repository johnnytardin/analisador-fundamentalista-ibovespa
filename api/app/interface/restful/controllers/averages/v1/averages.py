import logging

from flask import request, jsonify
from flask_restplus import Namespace, Resource

from app.application.averages import moving_averages, columns


api = Namespace("averages", description="Moving Averages Informations")
logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class AveragesQueryController(Resource):
    def post(self):
        code = request.json.get("targets")[0].get("target")
        summary = moving_averages(code)
        return [{"type": "table", "rows": summary, "columns": columns()}], 200


class AveragesSearchController(Resource):
    def post(self):
        return {"target": ""}, 200


api.add_resource(Health, "/", methods=["GET"])
api.add_resource(AveragesQueryController, "/query", methods=["POST"])
api.add_resource(AveragesSearchController, "/search", methods=["POST"])
