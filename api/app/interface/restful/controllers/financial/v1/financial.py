import logging

from flask import request, jsonify
from flask_restplus import Namespace, Resource

from app.application.financial import get_summary, columns


api = Namespace("financial", description="Financial Informations")
logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class FinancialQueryController(Resource):
    def post(self):
        code = request.json.get("targets")[0].get("target")
        summary = [get_summary(code)]
        return [{"type": "table", "rows": summary, "columns": columns()}], 200


class FinancialSearchController(Resource):
    def post(self):
        return {"target": ""}, 200


api.add_resource(Health, "/", methods=["GET"])
api.add_resource(FinancialQueryController, "/query", methods=["POST"])
api.add_resource(FinancialSearchController, "/search", methods=["POST"])
