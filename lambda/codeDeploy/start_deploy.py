import json
import boto3
import logging

client = boto3.client('codedeploy')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

applicationName = ''
deploymentGroupName = ''
S3bucketName = '' # The 'appspec.yml' file needs to exist in the S3 bucket

def lambda_handler(event, context):
    logger.info("Start Deploy")

    # See if there is a running deployment.
    listDeployments = client.list_deployments(
        applicationName=applicationName,
        deploymentGroupName=deploymentGroupName,
        includeOnlyStatuses=['InProgress'],
    )

    deployId = ''

    if(listDeployments['deployments']):
        deployId = listDeployments['deployments'][0]

    # If there is a running deployment task, stop immediately and stop rolling back the code.
    if(deployId):
        stopDeployment = client.stop_deployment(
            deploymentId=deployId,
            autoRollbackEnabled=False
        )

    # Start to create a new deployment task to redeploy.
    response = client.create_deployment(
        applicationName=applicationName,
        deploymentGroupName=deploymentGroupName,
        deploymentConfigName='CodeDeployDefault.ECSAllAtOnce',
        description='',
        revision={
            'revisionType': 'S3',
            's3Location': {
                'bucket': S3bucketName,
                'key': 'appspec.yml',
                'bundleType': 'YAML'
            }
        }
    )

    logger.info(response)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }

