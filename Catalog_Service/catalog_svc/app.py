import os
import sys

from flask import Flask

from .db import DB_URI
from .extensions import db

from .routes.health import health
from .routes.items import items
from .routes.item_lines import item_lines
from .routes.orders import orders
from .routes.static import static

cwd = os.getcwd()
sys.path.append(cwd)

print("*** PYHTHONPATH = " + str(sys.path) + "***")


def create_app():
    app = Flask(__name__, static_url_path="/static", static_folder="WebSite/static")
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

    db.app = app
    db.init_app(app)

    app.register_blueprint(health, url_prefix="")
    app.register_blueprint(static, url_prefix="")
    app.register_blueprint(items, url_prefix="/api")
    app.register_blueprint(item_lines, url_prefix="/api")
    app.register_blueprint(orders, url_prefix="/api")

    return app


application = create_app()
