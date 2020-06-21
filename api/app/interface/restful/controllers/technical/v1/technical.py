import logging

from flask import request, jsonify
from flask_restplus import Namespace, Resource

from app.application.technical import indicators, columns


api = Namespace("technical", description="Techinical Informations")
logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class TechnicalQueryController(Resource):
    def post(self):
        code = request.json.get("targets")[0].get("target")
        summary = [indicators(code)]
        return [{"type": "table", "rows": summary, "columns": columns()}], 200


class TechnicalSearchController(Resource):
    def post(self):
        return {"target": ""}, 200


api.add_resource(Health, "/", methods=["GET"])
api.add_resource(TechnicalQueryController, "/query", methods=["POST"])
api.add_resource(TechnicalSearchController, "/search", methods=["POST"])
