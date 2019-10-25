"""Handler."""
import json
import logging
import os
from collections import defaultdict

from addict import Dict
import boto3
from botocore.exceptions import ClientError

from exceptions import BadRequestError, ServerError
import enrich

LOG = logging.getLogger('generate_metric_alarms')


def process_alert(event):
    """Handles a new event request
    Placeholder copied from alert_controller implementation
    """
    LOG.info(str(event))
    return create_response(200, body='All good')


def create_response(status_code, status_description='', body=''):
    """Configure a response JSON object."""
    response = {
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html;"
        }
    }

    if not status_description:
        description = {
            200: '200 OK',
            400: '400 Bad Request',
            401: '401 Unauthorized',
            405: '405 Method Not Allowed',
            500: '500 Internal Server Error'
        }
        status_description = description.get(status_code)

    response['statusCode'] = status_code
    response['statusDescription'] = status_description
    response['body'] = body

    return response


def create_sns_message(alert):
    """Create the message to publish to SNS"""
    try:
        payload = json.dumps({"alert": alert})

        message = json.dumps({
            "default": "Default payload",
            "sqs": payload,
            "lambda": payload
        })
        LOG.debug('MESSAGE: %s', message)

        return message
    except TypeError as err:
        raise ServerError('Error creating SNS message') from err


def publish_alert(message, topic_arn):
    """Publish alert message to SNS"""
    try:
        sns = boto3.client('sns')
        sns_response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='New report-phishing alert recorded',
            MessageStructure='json'
        )
        LOG.debug('SNS Response: %s', sns_response)
        LOG.info('Alert published to SNS')

        return sns_response
    except ClientError as err:
        raise ServerError('Error publishing message to SNS') from err


def get_regions():
    """Get list of all AWS regions"""
    client = boto3.client("ec2")
    response = client.describe_regions()
    regions = [region["RegionName"] for region in response["Regions"]]
    return regions


def get_region_metrics():
    """Call cloudwatch list-metrics for each region and collate results"""
    regions = get_regions()
    region_metrics = defaultdict(list)

    for region in regions:
        type_metrics = defaultdict(list)
        print(f"Reading metrics for {region}")
        client = boto3.client("cloudwatch", region_name=region)
        response = Dict(client.list_metrics())
        for metric in response.Metrics:
            metric.Region = region
            metric_tags = enrich.get_tags_for_metric_resource(metric, region=region)
            metric.Tags = metric_tags
            component_type = metric.Namespace
            type_metrics[component_type].append(metric)
        region_metrics[region] = type_metrics

    return region_metrics


def get_caller():
    """Get caller based on current AWS credentials"""
    client = boto3.client("sts")
    response = Dict(client.get_caller_identity())
    return response


if __name__ == "__main__":
    """Initial development of list-metrics processing logic
    Enrich with tags
    """
    metrics = get_region_metrics()
    metric_data = json.dumps(metrics, indent=2)
    caller_response = get_caller()
    account = caller_response.Account
    file_path = f"output/{account}/"
    os.makedirs(file_path)
    var_file = open(f"{file_path}/metrics.json", "w")
    var_file.write(metric_data)
