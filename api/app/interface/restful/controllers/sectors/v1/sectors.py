import logging

from flask_restplus import Namespace, Resource

from app.application import sectors


api = Namespace("sectors", description="Sectors")
logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class SectorsQueryController(Resource):
    def post(self):
        return [{"type": "table", "rows": [], "columns": ["codes"]}], 200

    def options(self):
        return [{"type": "table", "rows": [], "columns": ["codes"]}], 200


class SectorsSearchController(Resource):
    def post(self):
        summary = sectors.get_sectors_names()
        return summary, 200

    def options(self):
        summary = sectors.get_sectors_names()
        return summary, 200


api.add_resource(Health, "/", methods=["GET"])
api.add_resource(SectorsQueryController, "/query", methods=["POST", "OPTIONS"])
api.add_resource(SectorsSearchController, "/search", methods=["POST", "OPTIONS"])
