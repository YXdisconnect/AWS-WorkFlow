++++++++++++++++++++++++lamda function 1 ++++++++++++++++++++++++++++++++
import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2022-07-23-17-14-30-760" ## TODO: fill in

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(image_data)

    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(ENDPOINT)

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")
    with open(image, "rb") as f:
        payload = f.read()

    # Make a prediction:
    inferences = predictor.predict(payload)

    # We return the data back to the Step Function    
    event["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }



++++++++++++++++++++++++lamda function 2 ++++++++++++++++++++++++++++++++
import json
# import sagemaker
import base64
# from sagemaker.serializers import IdentitySerializer
import boto3



# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2022-07-23-17-14-30-760" 
runtime = boto3.Session().client('sagemaker-runtime')

def lambda_handler(body, context):
    print("Received event: " + json.dumps(body, indent=2))
    
    # Decode the image data
    # data = json.loads(json.dumps(body['image_data']))
    body = json.loads(json.dumps(body))
    payload = body.get('image_raw')
    print(payload)
    image = base64.b64decode(payload)
    # print(image)

    # Instantiate a Predictor
    # predictor = sagemaker.predictor.Predictor(ENDPOINT)
    
    
    # For this model the IdentitySerializer needs to be "image/png"
    # predictor.serializer = IdentitySerializer("image/png")
    # with open(image, "rb") as f:
    #     payload = f.read()
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType = 'image/png',Body = image)
    print(response)
    
    # Make a prediction:
    result = json.loads(response['Body'].read().decode())
    print(result)
 

    # We return the data back to the Step Function    
    # event["result"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
    
    
++++++++++++++++++++++++lamda function 3 ++++++++++++++++++++++++++++++++
import json


THRESHOLD = .93


def lambda_handler(event, context):

    # Grab the inferences from the event
    print("Received event: " + json.dumps(event, indent=2))
   
    inferences = json.loads(json.dumps(event['body']))
    print(inferences)

    # Check if any values in our inferences are above THRESHOLD
    key = inferences[1:-2]
    print(key)
    key_to_list = key.split(',')
    meets_threshold = float(key_to_list[0]) > THRESHOLD

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }    