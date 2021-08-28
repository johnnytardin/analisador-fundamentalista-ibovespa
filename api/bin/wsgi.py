from config.config import config
from decouple import config as dconfig

from api import app

if __name__ == "__main__":
    app.run(
        debug=dconfig("API_DEBUG", config.debug or False),
        host=dconfig("API_BIND", config.host or "0.0.0.0"),
        port=dconfig("PORT", config.port or 5000),
    )
