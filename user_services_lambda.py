import boto3
import json
from botocore.vendored import requests

dynamo = boto3.client('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print(context)

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }
    operation = event['eventName']
    endpoint = event['endpoint']

    if operation in operations:
        if operation == "POST" and endpoint == "/users":
            add_user(event)


def add_user(event):
    email = event["email"]
    password = event["password"]
    last_name = event["last_name"]
    first_name = event["first_name"]
    
    email_json = json.dumps(email)
    password_json = json.dumps(password)
    last_name_json = json.dumps(last_name)
    first_name_json = json.dumps(first_name)
    
    payload = {"email": email_json, "password": password_json, "last_name": last_name_json, "first_name": first_name_json}
    
    # Send the POST request with payload to api endpoint
    request = requests.post('http://userservice-env-2.eba-kfpu9zpu.us-east-1.elasticbeanstalk.com/users', json=payload)
    
    return {
        "fulfillmentState": "POST SUCCESSFUL",
        "message": {
            "response": "Succesfully posted",
            "data" : payload
        }
    }
