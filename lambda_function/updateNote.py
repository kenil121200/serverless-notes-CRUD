import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')

def lambda_handler(event, context):
    data = json.loads(event['body'])
    
    # Prepare the update expression and attribute values
    update_expression = 'SET content = :content'
    expression_attribute_values = {':content': data['content']}
    
    # Only update imageUrl if it's not null
    if data.get('imageUrl') is not None:
        update_expression += ', imageUrl = :imageUrl'
        expression_attribute_values[':imageUrl'] = data['imageUrl']
    
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