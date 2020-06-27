import logging

from flask import request
from flask_restplus import Namespace, Resource

from app.application import magic_formula


api = Namespace("magic", description="Magic Formula")

logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class MagicRoicQueryController(Resource):
    def post(self):
        c = magic_formula.columns()
        r = magic_formula.ev_ebit_roic_query(request.json)
        return [{"type": "table", "rows": r, "columns": c}], 200


class MagicRoicSearchController(Resource):
    def post(self):
        return {"target": ""}, 200


class MagicPlQueryController(Resource):
    def post(self):
        c = magic_formula.columns()
        r = magic_formula.pl_roe_query(request.json)
        return [{"type": "table", "rows": r, "columns": c}], 200


api.add_resource(Health, "/roic/", methods=["GET"])
api.add_resource(Health, "/pl/", methods=["GET"])

api.add_resource(MagicRoicQueryController, "/roic/query", methods=["POST"])
api.add_resource(MagicPlQueryController, "/pl/query", methods=["POST"])
api.add_resource(MagicRoicSearchController, "/roic/search", methods=["POST"])
api.add_resource(MagicPlQueryController, "/pl/search", methods=["POST"])
