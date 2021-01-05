import json
import boto3

client = boto3.client("sns", region_name="us-east-1")

filters = {
    "/api/registrations": {
        "methods": ["POST"],
        "topic": "arn:aws:sns:us-east-1:558439013726:update_user",
    }
}


def publish_string(topic, json_data):
    s = json.dumps(json_data, default=str)

    print("emiting ", s, "to ", topic)
    result = client.publish(TopicArn=topic, Message=s)

    return result


def notify(request, response):
    path = request.path
    method = request.method
    body = request.json

    filter = filters.get(path, None)

    if filter is not None:
        if method in filter["methods"]:
            event = {
                "resource": path,
                "method": method,
                "data": body,
                "email": body["email"],
                "token": response.headers["Authentication"],
            }

            topic = filter["topic"]

            publish_string(topic, event)
