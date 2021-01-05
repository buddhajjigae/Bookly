import boto3
import json

from botocore.exceptions import ClientError

print("Loading function")
dynamo = boto3.client("dynamodb")


def send_email_verification(user_data):
    client = boto3.client("ses")

    SENDER = "Gitpull Worldwide <yy2608@columbia.edu>"
    RECIPIENT = user_data["data"]["email"]

    AWS_REGION = "us-east-1"
    SUBJECT = "COMSE6156 Milestone Email Verification"

    token_value = user_data["token"]
    email_verification_link = (
        "https://7amefvdrc7.execute-api.us-east-1.amazonaws.com/default/email_verification?token="
        + token_value
    )

    BODY_TEXT = (
        "COMSE6156 Milestone Email Verification\r\n"
        "Please click the link to verify your email " + email_verification_link
    )

    # The HTML body of the email.
    BODY_HTML = """<html>
        <head></head>
        <body>
          <p>Please click the link to verify your email <a href='{0}'>{0}</a></p>
        </body>
        </html>
    """

    BODY_HTML = BODY_HTML.format(email_verification_link)
    CHARSET = "UTF-8"

    try:
        response = client.send_email(
            Destination={
                "ToAddresses": [
                    RECIPIENT,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": BODY_HTML,
                    },
                    "Text": {
                        "Charset": CHARSET,
                        "Data": BODY_TEXT,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        print("Email sent! Message ID:"),
        print(response["MessageId"])


def respond(err, res=None):
    return {
        "statusCode": "400" if err else "200",
        "body": err.message if err else json.dumps(res),
        "headers": {
            "Content-Type": "application/json",
        },
    }


def lambda_handler(event, context):
    user_data = json.loads(event["Records"][0]["Sns"]["Message"])
    send_email_verification(user_data)

    return respond(None, {})
