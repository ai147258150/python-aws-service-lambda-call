# RDS backup S3
import json
import boto3

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('rds')

def lambda_handler(event, context):

    snapshots_data = client.describe_db_cluster_snapshots(
        DBClusterIdentifier='',
        SnapshotType='automated',
        Filters=[
            {
                'Name': 'db-cluster-id',
                'Values': [
                    'RDS ARN',
                ]
            }
        ]
    )

    task_identifier = snapshots_data['DBClusterSnapshots'][0]['DBClusterSnapshotIdentifier']

    snapshots_source_arn = 'RDS snapshot ARN' + task_identifier

    logger.info(task_identifier)
    logger.info(snapshots_source_arn)

    response = client.start_export_task(
        ExportTaskIdentifier=task_identifier.replace('rds:', ''),
        SourceArn=snapshots_source_arn,
        S3BucketName='',
        IamRoleArn='',
        KmsKeyId='',
        S3Prefix=''
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
