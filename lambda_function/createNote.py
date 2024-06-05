import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def lambda_handler(event, context):
    data = json.loads(event['body'])
    item = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'content': data['content'],
        'imageUrl': data['imageUrl']
    }
    table.put_item(Item=item)
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
        },
        'body': json.dumps(item),
    }