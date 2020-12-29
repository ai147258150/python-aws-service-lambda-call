import json
import boto3

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# SQS config
MAIN_QUEUE_URL = 'queue ARN'

sqs_client = boto3.client('sqs', region_name='region_name')

def lambda_handler(event, context):

    title = event['title']
    Author = event['Author']
    content = event['content']

    sqs_client.send_message(
        QueueUrl=MAIN_QUEUE_URL,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': str(title)
            },
            'Author': {
                'DataType': 'String',
                'StringValue': str(Author)
            },
        },
        MessageBody=str(content)
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
