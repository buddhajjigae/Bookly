import boto3
import json
import urllib3
from urllib import request

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
    # Print event body
    print("Received event: " + json.dumps(event, indent=2))
    
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }
    operation = event['eventName']
    endpoint = event['endpoint']

    # Make sure valid operation received
    if operation in operations:
        # For GET on all items
        if operation == "GET" and endpoint == "/comments":
            get_comments(event)
        # For PUT on items
        if operation == "PUT":
            sub_endpoint = endpoint[0:10]
            comment_number = endpoint[10:]
            # For PUT on updating an order
            if sub_endpoint == "/comments/":
                order_update(event, comment_number)
                

def get_comments(event):
    api = "CHANGE THIS/comments/"
    http = urllib3.PoolManager()
    # Send GET request to api endpoint
    request = http.request('GET',api)
    
    # Obtain the response data and HTTP status 
    http_status = request.status
    data = request.data
    print(http_status)
    print(data)
    
    if http_status == 200:
        return {
            "fulfillmentState": "GET SUCCESSFUL",
            "message": {
                "data": data
            }
        }
        
    return {
        "fulfillmentState": "GET FAILED"
    }

def update_comment(event, comment_number):
    http = urllib3.PoolManager()
    api = "CHANGE THIS" +  comment_number
    user = event["user"]
    text = event["text"]
    tags = event["tags"]
    
    payload = {"user": user, "text": text, "tags", tags}
    encoded_data = json.dumps(payload).encode('utf-8')
    
    # Send the PUT request with payload to the api endpoint
    request = http.request(
     'PUT',
     api,
     body=encoded_data,
     headers={'Content-Type': 'application/json'})
    
    # Obtain the response data and HTTP status 
    http_status = request.status
    data = json.loads(request.data.decode('utf-8'))
    print(http_status)
    print(data)
    
    if http_status == 200:
        return {
            "fulfillmentState": "PUT SUCCESSFUL",
            "message": {
                "data": data
            }
        }
        
    return {
        "fulfillmentState": "PUT FAILED"
    }
