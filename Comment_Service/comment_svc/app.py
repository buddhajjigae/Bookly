import os
import sys

from flask import Flask

from .routes.comments import comments
from .routes.health import health
from .routes.static import static
from .routes.responses import responses

cwd = os.getcwd()
sys.path.append(cwd)

print("*** PYHTHONPATH = " + str(sys.path) + "***")


def create_app():
    app = Flask(__name__, static_url_path="/static", static_folder="WebSite/static")
    app.config["DEBUG"] = True

    app.register_blueprint(health, url_prefix="")
    app.register_blueprint(static, url_prefix="")
    app.register_blueprint(comments, url_prefix="/api")
    app.register_blueprint(responses, url_prefix="/api")

    return app


application = create_app()
