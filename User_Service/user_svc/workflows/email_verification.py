import boto3
import json
import jwt
import requests

from botocore.exceptions import ClientError

print("Loading function")
dynamo = boto3.client("dynamodb")


def respond(err, res=None):
    return {
        "statusCode": "400" if err else "200",
        "body": err.message if err else json.dumps(res),
        "headers": {
            "Content-Type": "application/json",
        },
    }


def lambda_handler(event, context):
    user_info = {}
    has_error = False

    try:
        token = event["queryStringParameters"]["token"]
        user_info = jwt.decode(
            token, "412h4fa8sg34tj,naif3205235h23k5", algorithms="HS256"
        )
    except:
        has_error = True

    if not has_error and user_info["email"] is not None:
        headers = {
            "Authentication": b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImYwZjE1NTQ2LTJhN2UtMTFlYi1hNzk0LTBhMDlkNjFjMDRiNSJ9.bZTJl1P5Az-EHSeyS9rv7ILwXOv7O5AlZSH94ebN7IE"
        }

        requests.put(
            "http://userservice-env-2.eba-kfpu9zpu.us-east-1.elasticbeanstalk.com/users/"
            + user_info["id"],
            data={},
            headers=headers,
        )

        return {
            "statusCode": "302",
            "headers": {
                "Location": "http://coms6156milestone.s3-website-us-east-1.amazonaws.com/static/index.html?"
                + "email="
                + user_info["email"]
                + "&first_name="
                + user_info["first_name"]
                + "&last_name="
                + user_info["last_name"]
            },
        }

    else:
        return {
            "statusCode": "302",
            "headers": {
                "Location": "http://coms6156milestone.s3-website-us-east-1.amazonaws.com/static/error.html"
            },
        }
