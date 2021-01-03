import json
import platform
import socket

from datetime import datetime
from flask import Response
from flask.blueprints import Blueprint

from catalog_svc.log import log_and_extract_input


health = Blueprint("health", __name__)


# This function performs a basic health check. We will flesh this out.
@health.route("/health", methods=["GET"])
def health_check():

    pf = platform.system()

    rsp_data = {
        "status": "healthy",
        "time": str(datetime.now()),
        "platform": pf,
        "release": platform.release(),
    }

    if pf == "Darwin":
        rsp_data["note"] = "For some reason, macOS is called 'Darwin'"

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    rsp_data["hostname"] = hostname
    rsp_data["IPAddr"] = IPAddr

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


@health.route("/demo/<parameter>", methods=["GET", "POST"])
def demo(parameter):

    inputs = log_and_extract_input(demo, {"parameter": parameter})

    msg = {"/demo received the following inputs": inputs}

    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp
