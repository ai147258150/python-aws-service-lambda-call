from botocore.exceptions import ClientError
import math
import boto3
import json

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sender = 'sender@163.com'
addressee = 'subscription@163.com'

def lambda_handler(event, context):

    email = event['address']
    email_subject = event['email_subject']
    email_body = event['content']

    # Process the received data format
    if isinstance(email, str) and ("[" in email or "]" in email):
        email = eval(email)


    if len(email) == 1:

        ses_email_send(email_subject, email_body, email[0], '')

    elif isinstance(email, str):

        ses_email_send(email_subject, email_body, email, '')

    elif isinstance(email, list):

        start_num = 0
        limit = 50
        send_num = math.ceil(len(email)/limit)

        # Since only 50 people can be BCC each time, more than 50 people will be sent in batches
        while start_num < send_num:
            start = start_num * limit
            end = start + limit
            send_list = email[start:end]
            start_num += 1
            ses_email_send(email_subject, email_body, addressee, send_list)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }


def ses_email_send(email_subject, email_body, ToAddresses, BccAddresses):

    ses_client = boto3.client('ses', region_name='region_name')

    Destinations = {
        'ToAddresses': [
            ToAddresses
        ]
    }

    if BccAddresses:
        Destinations.update({'BccAddresses': BccAddresses})

    try:
        # Provide the contents of the email.
        response = ses_client.send_email(
            Destination=Destinations,
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': email_body,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': email_subject,
                },
            },
            Source=sender,
        )

    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        status = 'Failure'
    else:
        logger.info("Email sent successfully! Message ID:" + response['MessageId'])
        status = 'Success'

    return status