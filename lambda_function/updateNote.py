import json
import boto3

dynamodb = boto3.resource('dynamodb') # Initialize DynamoDB resource using boto3
table = dynamodb.Table('Notes') # Specify the DynamoDB table we're using

def lambda_handler(event, context):
    data = json.loads(event['body'])
    
    # Prepare the update expression and attribute values
    update_expression = 'SET content = :content'
    expression_attribute_values = {':content': data['content']}
    
    # Only update imageUrl if it's not null
    if data.get('imageUrl') is not None:
        update_expression += ', imageUrl = :imageUrl'
        expression_attribute_values[':imageUrl'] = data['imageUrl']
    
    # Update the note in the DynamoDB table
    table.update_item(
        Key={
            'id': event['rawPath'].lstrip('/')
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
        },
        'body': json.dumps({'message': 'Note updated'})
    }