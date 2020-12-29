import json
import boto3
import uuid

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

step_client = boto3.client('stepfunctions')

step_arn = 'step function ARN'

def lambda_handler(event, context):

    json_body = event['Records'][0]

    # Receive sqs message parameters
    content = str(json_body['body'])
    address = str(json_body['messageAttributes']['address']['stringValue'])
    message_type = str(json_body['messageAttributes']['messageType']['stringValue'])
    email_subject = str(json_body['messageAttributes']['email_subject']['stringValue'])

    input_data = "{\"address\": \"" + address + "\", \"email_subject\": \"" + email_subject + "\", \"content\": \"" + content + "\"}"

    logger.info(input_data)

    # Generate unique name
    step_name = str(uuid.uuid1()) + '-' +str(message_type)

    # Start function
    response = step_client.start_execution(
        stateMachineArn=step_arn,
        name=step_name,
        input=input_data
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
