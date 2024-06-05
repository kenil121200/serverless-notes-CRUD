import json
import boto3

dynamodb = boto3.resource('dynamodb') # Initialize DynamoDB resource using boto3
table = dynamodb.Table('Notes') # Specify the DynamoDB table we're using

def lambda_handler(event, context):
    response = table.scan() # Scan the entire DynamoDB table
    return {
        'statusCode': 200,
        'headers': {
                "Content-Type": "application/json",
        },
        'body': json.dumps(response['Items'])
    }