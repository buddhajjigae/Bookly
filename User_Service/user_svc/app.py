import os
import sys

from flask import Flask

from .db import DB_URI
from .extensions import db
from .routes.addresses import addresses
from .routes.google_auth import google_auth
from .routes.health import health
from .routes.static import static
from .routes.users import users

cwd = os.getcwd()
sys.path.append(cwd)

print("*** PYHTHONPATH = " + str(sys.path) + "***")


def create_app():
    app = Flask(__name__, static_url_path="/static", static_folder="WebSite/static")
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.secret_key = os.urandom(24)

    db.app = app
    db.init_app(app)

    app.register_blueprint(health, url_prefix="")
    app.register_blueprint(static, url_prefix="")
    app.register_blueprint(addresses, url_prefix="/api")
    app.register_blueprint(users, url_prefix="/api")
    app.register_blueprint(google_auth, url_prefix="/api")

    return app


application = create_app()
