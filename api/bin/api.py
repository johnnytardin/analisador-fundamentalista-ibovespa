import os
import logging

from flask import Flask, url_for
from flask_restplus import Api
import json_logging

import fixpath  # noqa

from config.config import config
from app.interface.restful.controllers import blueprints
from decouple import config as dconfig


app = Flask(__name__)
api = Api(app)


if os.environ.get('PORT'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')
 
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
        debug=os.getenv("API_DEBUG", config.debug or False),
        host=os.getenv("API_BIND", config.host or "0.0.0.0"),
        port=dconfig("PORT", 5000)
    )
