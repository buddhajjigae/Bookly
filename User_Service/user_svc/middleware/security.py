import jwt

from user_svc.models.user import User
from user_svc.workflows.jwt_config import secret_key as secret

_white_list = {
    "/",
    "/api/registrations",
    "/api/login",
}


def decode_token(token):
    user_info = jwt.decode(token, secret, algorithms="HS256")["id"]

    return user_info


def check_authentication(request):
    result = (401, "NOT AUTHORIZED", None)

    try:
        if not request.path in _white_list:
            header = dict(request.headers)
            token = header.get("Authentication", None)

            if token is not None:
                user_id = decode_token(token)

                user_info = User.query.filter_by(id=user_id).first()

                if user_info:
                    result = (200, "OK", user_info)
                else:
                    result = (403, "Forbidden error", None)
        else:
            result = (200, "OK", None)

    except Exception as e:
        print("Error: ", e)

    return result
