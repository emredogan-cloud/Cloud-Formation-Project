import boto3
import logging
import os
import json
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    region = os.environ.get('AWS_REGION', 'us-east-1')
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')

    ec2 = boto3.client('ec2', region_name=region)
    sns = boto3.client('sns', region_name=region) 
    
    orphan_volumes = []

    try:
        paginator = ec2.get_paginator('describe_volumes')
        page_iterator = paginator.paginate(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )

        for page in page_iterator:
            for vol in page.get('Volumes', []):
                v_id = vol['VolumeId']
                v_size = vol['Size']
                orphan_volumes.append(v_id)
                logger.info(f"FOUND: {v_id}")

        if orphan_volumes and sns_topic_arn:
            volume_list_str = "\n".join(orphan_volumes)
            
            message_text = (
                f"WARNING! {len(orphan_volumes)} Unclaimed EBS volumes detected in {region}.\n\n"
                f"List of Volumes:\n{volume_list_str}\n\n"
                "Please take action to delete or archive these resources."
            )
            
            sns.publish(
                TopicArn=sns_topic_arn,
                Message=message_text,
                Subject=f'AWS Orphan Resource Report - {region}'
            )
            
            logger.info(f"SNS notification sent to {sns_topic_arn}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Scanning complete.',
                'count': len(orphan_volumes)
            })
        }

    except ClientError as e:
        logger.error(f"ERROR: {e}")
        return {'statusCode': 500, 'body': str(e)}
