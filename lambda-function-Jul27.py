++++++++++++++++++++++++ Lambda function for image serialization  +++++++++++++++++++++++++++
mport json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = "test/bicycle_s_000513.png"  ## TODO: fill in
    bucket = "sagemaker-us-east-2-622818390027" ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, '/tmp/image.png')
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    # print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

++++++++++++++++++++++++ lambda function for inferene  +++++++++++++++++++++++++++
import json
import base64
import boto3

ENDPOINT = "image-classification-2022-07-23-17-14-30-760"
runtime= boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    # json.loads(json.dumps(event))
    # print(type(event))
    # print(event['iamge_data'])
    image = base64.b64decode(event['body']['image_data'])
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='application/x-image', Body=image)
    inferences = response['Body'].read().decode('utf-8')
    event["inferences"] = [float(x) for x in inferences[1:-1].split(',')] 
    return {
        'statusCode': 200,
        'body': {
            "inferences": event['inferences']
        }
    }
 

++++++++++++++++++++++++ lambda function for filter   +++++++++++++++++++++++++++

import json


THRESHOLD = .93


def lambda_handler(event, context):

    # Grab the inferences from the event
    inferences = event['body']['inferences']
    print(inferences)

    # Check if any values in our inferences are above THRESHOLD
    # key = inferences[1:-2]
    # print(key)
    # key_to_list = key.split(',')
    a = inferences[0]
    meets_threshold = float(a) > THRESHOLD

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    
    if meets_threshold:
        pass
    else:
        raise TypeError ("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
