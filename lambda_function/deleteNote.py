import json
import boto3
import traceback

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('Notes')

def lambda_handler(event, context):
    try:
        id = event['rawPath'].lstrip('/')
        
        # Fetch the note from the database
        response = table.get_item(Key={'id': id})
        note = response['Item']
        
        # If the note has an image URL, delete the image from S3
        if note.get('imageUrl'):
            url = note['imageUrl']
            filename = url.split("/")[-1]
            
            # Only delete the object if filename is not empty
            if filename:
                s3.delete_object(Bucket='notes-images-serverless-app', Key=filename)

        # Delete the note from the database
        table.delete_item(Key={'id': id})

        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json",
            },
            'body': json.dumps({'message': 'Note deleted'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                "Content-Type": "application/json",
            },
            'body': json.dumps({'message': 'An error occurred'})
        }