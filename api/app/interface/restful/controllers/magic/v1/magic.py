import logging

from flask import request, jsonify
from flask_restplus import Namespace, Resource

from app.application.magic_formula import MagicFormula


api = Namespace("magic", description="Magic Formula")

logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class MagicSearchController(Resource):
    def post(self):
        return [], 200


class MagicRoicQueryController(Resource):
    def post(self):
        c = MagicFormula.columns()
        r = MagicFormula.ev_ebit_roic_query()
        return [{"type": "table", "rows": r, "columns": c}], 200


class MagicRoicSearchController(Resource):
    def post(self):
        return {"target": ""}, 200


class MagicPlQueryController(Resource):
    def post(self):
        c = MagicFormula.columns()
        r = MagicFormula.pl_roe_query()
        return [{"type": "table", "rows": r, "columns": c}], 200


api.add_resource(Health, "/roic/", methods=["GET"])
api.add_resource(Health, "/pl/", methods=["GET"])

api.add_resource(MagicRoicQueryController, "/roic/query", methods=["POST"])
api.add_resource(MagicPlQueryController, "/pl/query", methods=["POST"])
api.add_resource(MagicRoicSearchController, "/roic/search", methods=["POST"])
api.add_resource(MagicPlQueryController, "/pl/search", methods=["POST"])
