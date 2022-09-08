import logging
from re import S

from app.application import sectors
from flask_restx import Namespace, Resource

api = Namespace("sectors", description="Sectors")
logger = logging.getLogger(__name__)


class Health(Resource):
    def get(self):
        return None, 200


class SectorsQueryController(Resource):
    def post(self):
        return [{"type": "table", "rows": [], "columns": ["codes"]}], 200


class SectorsSearchController(Resource):
    def post(self):
        s = []
        for sector in sectors.get_sectors_names():
            s.append({"sector": sector})

        return s, 200


api.add_resource(Health, "/", methods=["GET"])
api.add_resource(SectorsQueryController, "/query", methods=["GET", "POST"])
api.add_resource(SectorsSearchController, "/variable", methods=["GET", "POST"])
