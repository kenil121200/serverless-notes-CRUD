import boto3
import base64
import uuid
import json
import os
from botocore.exceptions import NoCredentialsError

# Initialize S3 client using boto3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])  # parse the body into a dictionary
        file_content = base64.b64decode(body['file'])
        original_file_name = body['filename']
        file_extension = os.path.splitext(original_file_name)[1]  # extract file extension
        file_path = str(uuid.uuid4()) + file_extension  # append file extension to UUID 
        bucket_name = 'notes-images-serverless-app'   # Specify the S3 bucket name

        # Upload the file to the S3 bucket
        s3.put_object(Body=file_content, Bucket=bucket_name, Key=file_path)
        # Generate the file URL
        file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_path}"

        
        return {
            'statusCode': 200,
            'body': json.dumps({'imageUrl': file_url}),
            'headers': {
                "Content-Type": "application/json",
            },
        }
    except NoCredentialsError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No AWS credentials found'}),
            'headers': {
                "Content-Type": "application/json",
            },
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                "Content-Type": "application/json",
            },
        }