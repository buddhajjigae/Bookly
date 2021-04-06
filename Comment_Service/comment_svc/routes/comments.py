import json

from flask import jsonify, request
from flask import Response as flask_response
from flask.blueprints import Blueprint

from comment_svc.resources.comments_table import CommentsTable
from comment_svc.models.comment import Comment

comments = Blueprint("comments", __name__)
comments_table = CommentsTable()

# /comments


@comments.route("/comments", methods=["GET"])
def get_comments():
    user = request.args.get("user")
    tag = request.args.get("tag")

    if user and not tag:
        user_comments = comments_table.get_comments_by_user(user)
        return jsonify(user_comments)

    if tag and not user:
        tagged_comments = comments_table.get_comments_by_tag(tag)
        return jsonify(tagged_comments)

    if tag and user:
        tagged_user_comments = comments_table.get_user_comments_by_tag(user, tag)
        return jsonify(tagged_user_comments)

    all_comments = comments_table.get_all_comments()
    return jsonify(all_comments)


@comments.route("/comments", methods=["POST"])
def add_comment():
    user_email = request.args["user"]
    text = request.args["text"]
    tags = request.args.get("tags", [])

    new_comment = Comment(user_email, text, tags)
    comments_table.create_comment(new_comment.as_dict)
    location = "/api/comments/" + new_comment.comment_id
    msg = {"Location:": location}

    rsp = flask_response(json.dumps(msg), status=201, content_type="application/json")
    return rsp


# /comments/<comment_id>


@comments.route("/comments/<comment_id>", methods=["GET"])
def get_comment_by_id(comment_id):
    comment = comments_table.get_comment_by_id(comment_id)

    return jsonify(comment)


@comments.route("/comments/<comment_id>", methods=["PUT"])
def update_comment(comment_id):
    new_version_id = request.args.get("version_id")

    if new_version_id is None:
        msg = "Must provide accurate version_id to perform comment update"
        rsp = flask_response(msg, status=400, content_type="application/json")
        return rsp

    new_user = request.args.get("user")
    new_text = request.args.get("text")
    new_tags = request.args.get("tags")

    update_response = comments_table.update_comment(
        comment_id, new_user, new_text, new_tags, new_version_id
    )

    msg = update_response["ResponseMetadata"]["ResponseMsg"]
    status = update_response["ResponseMetadata"]["HTTPStatusCode"]

    rsp = flask_response(msg, status=status, content_type="application/json")
    return rsp
