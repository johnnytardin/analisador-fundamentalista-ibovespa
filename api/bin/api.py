import logging
import os

import fixpath  # noqa
import json_logging
from app.interface.restful.controllers import blueprints
from config.config import config
from decouple import config as dconfig
from flask import Flask, url_for
from flask_restplus import Api

app = Flask(__name__)
api = Api(app)


if os.environ.get("DYNO"):

    @property
    def specs_url(self):
        return url_for(self.endpoint("specs"), _external=True, _scheme="https")

    Api.specs_url = specs_url


logging.basicConfig(level="DEBUG" if config.debug else "INFO")
if config.enable_json_logging:
    json_logging.init_flask(enable_json=True)
    json_logging.config_root_logger()
    json_logging.init_request_instrument(app)


for blueprint, api in blueprints:
    app.register_blueprint(blueprint)


if __name__ == "__main__":
    app.run(
        debug=dconfig("API_DEBUG", config.debug or False),
        host=dconfig("API_BIND", config.host or "0.0.0.0"),
        port=dconfig("PORT", config.port or 5000),
    )
