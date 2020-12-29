import json
import boto3
import time
import hashlib
import logging

import dynamo_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB client
dynamo_client = boto3.client('dynamodb',region_name=dynamo_config.region_name,aws_access_key_id=dynamo_config.aws_access_key_id, aws_secret_access_key=dynamo_config.aws_secret_access_key)

table = 'DynamoDB Name'

def lambda_handler(event, context):

    title = event['title']

    timeStamp = int(time.time())
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))

    log_id = hashlib.md5(str(time.time()).encode()).hexdigest()

    item = {'log_id': {'S': log_id},
            'title': {'S': title},
            'now_time': {'S': now_time}
            }

    try:
        dynamo_client.put_item(TableName=table, Item=item)
        logger.info('File version has been added DynamoDB. ')
    except Exception as e:
        logger.error('ERROR: put item fail. msg: ' + str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
