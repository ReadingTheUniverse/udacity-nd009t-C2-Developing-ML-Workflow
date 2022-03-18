'''
This is an AWS lambda function that extracts images from S3 and serializes them into base64.

Author:  Luis Martinez

Project: Udacity AWS Machine Learning Engineer Nanodegree - Project 2 - Build a ML Workflow For Scones On AWS SageMaker

'''

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['body']['s3_key']
    bucket = event['body']['s3_bucket']

    # Download the data from s3 to /tmp/image.png
    image = '/tmp/image.png'
    s3.download_file(bucket, key, image)

    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }
