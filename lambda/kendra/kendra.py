import json
import boto3
import base64

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

kendra = boto3.client('kendra', 'region_name')

kendra_index_id = ''

def lambda_handler(event, context):

    body_post = event['body']

    result = base64.b64decode(body_post)

    result = str(result, 'utf-8')

    json_body = json.loads(result)

    logger.info(json_body)

    query = json_body[0]['keywords']
    page = int(json_body[0]['page'])

    try:
        limit = int(json_body[0]['limit'])
    except:
        limit = 10

    # Inquire
    query_data = kendra.query(IndexId=kendra_index_id, QueryText=query, PageNumber=page, PageSize=limit)

    response = {'total_number': query_data['TotalNumberOfResults'], 'result_items': query_data['ResultItems']}

    logger.info(response)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
