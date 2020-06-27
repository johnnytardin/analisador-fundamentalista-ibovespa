import os
import logging

from flask import Flask
from flask_restplus import Api
import json_logging

import fixpath  # noqa

from config.config import config
from app.interface.restful.controllers import blueprints


app = Flask(__name__)
api = Api(app)


logging.basicConfig(level="DEBUG" if config.debug else "INFO")
if config.enable_json_logging:
    json_logging.init_flask(enable_json=True)
    json_logging.config_root_logger()
    json_logging.init_request_instrument(app)


for blueprint, api in blueprints:
    app.register_blueprint(blueprint)


if __name__ == "__main__":
    app.run(
        debug=os.getenv("API_DEBUG", config.debug or False),
        host=os.getenv("API_BIND", config.host or "0.0.0.0"),
        port=os.getenv("API_PORT", config.port or 5000),
    )
