from flask import Response
from flask.blueprints import Blueprint

from comment_svc.static import welcome


static = Blueprint("static", __name__)


@static.route("/")
def index():
    rsp = Response(welcome, status=200, content_type="text/html")
    return rsp
