import os
import json
import yaml

from types import SimpleNamespace


class Config:
    def __init__(self, file):
        self.struct = self._struct(
            self._yaml_load(
                os.path.dirname(os.path.realpath(__file__)) + f"/{file}.yml"
            )
        )

    def _struct(self, __dict__):
        return json.loads(
            json.dumps(__dict__), object_hook=lambda d: SimpleNamespace(**d)
        )

    def _yaml_load(self, file):
        with open(file) as __file__:
            return yaml.safe_load(__file__)


config = Config(os.getenv("ENVIRONMENT", "staging")).struct
