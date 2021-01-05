import json
import jwt
import uuid
import os

from datetime import datetime
from flask import request, Response, jsonify, abort
from flask.blueprints import Blueprint

# this import is used to create a hashed password
from werkzeug.security import generate_password_hash, check_password_hash

from user_svc.workflows.notification import notify
from user_svc.workflows.jwt_config import secret_key as secret
from user_svc.extensions import db
from user_svc.routes.google_auth import is_logged_in, get_user_info
from user_svc.models.user import User, UserSchema
from user_svc.middleware.security import check_authentication

users = Blueprint("users", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
users.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)


# endpoint to show all users
@users.route("/users/", methods=["GET"])
@users.route("/users/page/<int:page>", methods=["GET"])
def get_users(page=None):
    per_page = None
    if page:
        per_page = 2

    all_users = User.query.paginate(page, per_page, error_out=False).items
    result = users_schema.dump(all_users)

    return jsonify(result)


@users.after_request
def after_decorator(response):
    notify(request, response)

    return response


@users.before_request
def before_decorator():
    precheck = check_authentication(request)

    if precheck[0] != 200:
        abort(precheck[0], precheck[1])


# endpoint to create new user
@users.route("/users", methods=["POST"])
def add_user():
    email = request.json["email"]
    password = request.json["password"]
    hashed_password = generate_password_hash(password)
    address_id = request.json["address_id"]
    last_name = request.json["last_name"]
    first_name = request.json["first_name"]
    user_uuid = str(uuid.uuid1())
    role = "1"
    timestamp = str(datetime.now())

    new_user = User(
        user_uuid,
        last_name,
        first_name,
        email,
        hashed_password,
        address_id,
        role,
        timestamp,
    )

    db.session.add(new_user)
    db.session.commit()

    location = "/api/users/" + user_uuid

    msg = {
        "timestamp": timestamp,
        "role": role,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": hashed_password,
        "address_id": address_id,
    }

    rsp = Response(
        json.dumps(msg, skipkeys=True, allow_nan=True),
        status=201,
        content_type="application/json",
    )

    return rsp


# endpoint to get user detail by id
@users.route("/users/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@users.route("/users/<id>", methods=["PUT"])
def user_update(id):
    # handle unauthorized requests
    header_user_id = jwt.decode(
        request.headers["Authentication"], secret, algorithms="HS256"
    )["id"]
    if header_user_id != "f0f15546-2a7e-11eb-a794-0a09d61c04b5":
        abort(401)

    user = User.query.get(id)
    user.status = "ACTIVE"
    db.session.commit()

    return user_schema.jsonify(user)


# endpoint to delete user
@users.route("/users/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


# endpoint to register new user
@users.route("/registrations", methods=["POST"])
def register_user():
    try:
        user_uuid = str(uuid.uuid1())
        email = request.json["email"]
        password = request.json["password"]
        # hashes the password
        hashed_password = generate_password_hash(password)
        address_id = request.json["address_id"]
        last_name = request.json["last_name"]
        first_name = request.json["first_name"]
        # role set to 1 for testing, we should standardize a user id to be an admin role
        role = "1"
        timestamp = str(datetime.now())

        token = jwt.encode(
            {
                "id": user_uuid,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "timestamp": timestamp,
            },
            secret,
            algorithm="HS256",
        )

        # these two lines are to test if the above is working properly
        msg = {
            "timestamp": timestamp,
            "role": role,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": hashed_password,
            "address_id": address_id,
        }

        # this is to form a response
        response = Response(
            json.dumps(msg, skipkeys=True, allow_nan=True),
            status=201,
            content_type="application/json",
        )
        # used to attach a header to the response
        response.headers["Authentication"] = token

        # add to the db
        new_user = User(
            user_uuid,
            last_name,
            first_name,
            email,
            hashed_password,
            address_id,
            role,
            timestamp,
        )

        db.session.add(new_user)
        db.session.commit()

        return response

    except Exception as e:
        return Response(
            json.dumps(
                "Duplicate email found. Registration must contain a unique email",
                skipkeys=True,
                allow_nan=True,
            ),
            status=400,
            content_type="application/json",
        )


@users.route("/login", methods=["POST"])
def login_user():
    user_info = User.query.filter_by(email=request.json["email"]).first()

    if not user_info:
        abort(401, "user/password not correct")

    if check_password_hash(user_info.hashed_password, request.json["password"]):
        token = jwt.encode(
            {"id": user_info.id, "email": user_info.email, "role": user_info.role},
            secret,
            algorithm="HS256",
        )  # .decode('utf-8')

        msg = {"message": "login success"}
        response = Response(
            json.dumps(msg, skipkeys=True, allow_nan=True),
            status=201,
            content_type="application/json",
        )
        response.headers["Authentication"] = token
    else:
        msg = {"message": "login failed"}
        response = Response(
            json.dumps(msg, skipkeys=True, allow_nan=True),
            status=403,
            content_type="application/json",
        )

    return response


@users.route("/googleLogin")
def index():
    if is_logged_in():
        user_info = get_user_info()
        return (
            "<div>You are currently logged in as "
            + user_info["given_name"]
            + "<div><pre>"
            + json.dumps(user_info, indent=4)
            + "</pre>"
        )

    return "You are not currently logged in."
