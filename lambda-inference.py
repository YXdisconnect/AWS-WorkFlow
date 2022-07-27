import json
import base64
import boto3


ENDPOINT = "image-*******"
runtime= boto3.client('runtime.sagemaker')
def lambda_handler(event, context):
    """A function to invoke endpoint"""
    image = base64.b64decode(event['image_data'])
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='application/x-image', Body=image)
    inferences = response['Body'].read().decode('utf-8')
    event["inferences"] = [float(x) for x in inferences[1:-1].split(',')] 
    return {
        'statusCode': 200,
        'body': {
            "image_data": event['image_data'],
            "s3_bucket": event['s3_bucket'],
            "s3_key": event['s3_key'],
            "inferences": event['inferences'],
        }
    }
