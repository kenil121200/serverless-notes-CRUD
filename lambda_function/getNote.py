import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def lambda_handler(event, context):
    response = table.scan()
    return {
        'statusCode': 200,
        'headers': {
                "Content-Type": "application/json",
        },
        'body': json.dumps(response['Items'])
    }