import json
import boto3
import os

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# transcoder config
output_prefix = 'video/'
region_name = ''
pipeline_id = '' # Create a transcoding pipeline in advance
preset_id_1080 = '' # Set ID

transcoder = boto3.client('elastictranscoder', region_name)

def lambda_handler(event, context):

    in_file = event['objectname']

    input_prefix = os.path.dirname(in_file) + "/"

    out_file = ('.'.join(in_file[len(input_prefix):].split('.')[:-1]) + '.mp4')

    transcoder.create_job(
        PipelineId=pipeline_id,
        Input={
            'Key': in_file,
            'FrameRate': 'auto',
            'Resolution': 'auto',
            'AspectRatio': 'auto',
            'Interlaced': 'auto',
            'Container': 'auto'
        },
        Outputs=[{
            'Key': output_prefix + '1080p/' + out_file,
            'PresetId': preset_id_1080
        }]
    )

    logger.info('File "' + in_file + '" is transcoding. ')

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
