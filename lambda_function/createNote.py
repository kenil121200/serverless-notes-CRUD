import json
import boto3
import uuid

# Initialize DynamoDB resource using boto3
dynamodb = boto3.resource('dynamodb')

# Specify the DynamoDB table we're using
table = dynamodb.Table('Notes')

# Define the AWS Lambda handler function
def lambda_handler(event, context):
    # Parse the incoming event body as JSON
    data = json.loads(event['body'])
    
    # Create a new item with a unique ID, and the title, content, and imageUrl from the event data
    item = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'content': data['content'],
        'imageUrl': data['imageUrl']
    }
    
    # Put the new item into the DynamoDB table
    table.put_item(Item=item)
    
    # Return a response with a 200 status code, JSON content type, and the item in the body
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
        },
        'body': json.dumps(item),
    }