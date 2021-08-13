from flask import Blueprint
from flask_restx import Api
from .magic import *
from .sectors import *
from .stocks import *
from .technical import *


def create_blueprint(description=str(), version=str(), prefix=str(), apis={}):
    blueprint = Blueprint(f"v{version}", __name__, url_prefix=prefix)

    bp_api = Api(
        blueprint,
        version=version,
        title=description,
        description=description,
    )

    for api in apis:
        bp_api.add_namespace(api)

    return blueprint, bp_api


blueprints = [
    create_blueprint(
        "Stocks API",
        "1",
        "/v1",
        {v1_magic, v1_technical, v1_stocks, v1_sectors},
    ),
]
