import json
import uuid

from flask import jsonify, request
from flask import Response as flask_response
from flask.blueprints import Blueprint

from comment_svc.resources.comments_table import CommentsTable
from comment_svc.models.response import Response

responses = Blueprint("responses", __name__)
comments_table = CommentsTable()

# /comments/<comment_id>/responses


@responses.route("/comments/<comment_id>/responses", methods=["GET"])
def get_responses(comment_id):
    comment = comments_table.get_comment_by_id(comment_id)
    all_responses = comment["responses"]

    return jsonify(all_responses)


@responses.route("/comments/<comment_id>/responses", methods=["POST"])
def add_response(comment_id):
    comment = comments_table.get_comment_by_id(comment_id)
    if not comment:
        rsp = flask_response(
            "Comment {} not found".format_map(comment_id),
            status=404,
            content_type="application/json",
        )
        return rsp

    user_email = request.args["user"]
    text = request.args["text"]
    response = Response(user_email, text)

    comments_table.add_response_to_comment(comment_id, response.as_dict)

    location = "/api/comments/{}/responses/{}".format(comment_id, response.response_id)
    msg = {"Location:": location}

    rsp = flask_response(json.dumps(msg), status=201, content_type="application/json")
    return rsp
