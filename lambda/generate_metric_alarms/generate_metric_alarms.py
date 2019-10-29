"""Handler."""
import json
import logging
import os
from collections import defaultdict

from addict import Dict
import boto3
from botocore.exceptions import ClientError

from local_exceptions import ServerError
import enrich
import format_terraform


LOG = logging.getLogger('generate_metric_alarms')


def process_alert(event):
    """Handles a new event request
    Placeholder copied from alert_controller implementation
    """
    LOG.info(str(event))
    return create_response(200, body='Response to HealthCheck')


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
        has_next_page = True
        next_page_token = None
        while has_next_page:
            if next_page_token:
                response = Dict(client.list_metrics(NextToken=next_page_token))
            else:
                response = Dict(client.list_metrics())

            has_next_page = "NextToken" in response
            if has_next_page:
                next_page_token = response.NextToken

            for metric in response.Metrics:
                metric.Region = region
                component_type = metric.Namespace
                type_metrics[component_type].append(metric)
        region_metrics[region] = type_metrics

    return region_metrics


def get_caller():
    """Get caller based on current AWS credentials"""
    client = boto3.client("sts")
    response = Dict(client.get_caller_identity())
    return response


def main():
    """Initial development of list-metrics processing logic
    Enrich with tags
    """
    metrics = get_region_metrics()

    caller_response = get_caller()
    file_path = f"output/{caller_response.Account}/"
    os.makedirs(file_path, exist_ok=True)

    alarms = Dict()

    # implement standard monitoring rules based on namespace
    for metric_rule in METRIC_RULES:
        namespace = metric_rule.Namespace
        service = enrich.get_namespace_service(namespace)
        if service not in alarms:
            alarms[service] = defaultdict(list)
        # print(str(metric_rule))
        for region in metrics:
            print(f"Analysing metrics for {region}\n")
            region_metrics = metrics[region]
            namespace_metrics = region_metrics[namespace]
            print(f"Found {len(namespace_metrics)} metrics for {namespace} in {region}\n")
            for metric in namespace_metrics:
                print(f"Checking rules for {metric.MetricName}")
                if metric.MetricName == metric_rule.MetricName:

                    # get tags for metric resource and add to metric
                    metric.Tags = enrich.get_tags_for_metric_resource(metric, region=region)

                    # get metric-statistics and calculate health threshold
                    metric.Threshold = enrich.get_metric_threshold(metric, metric_rule)

                    # annotate with service
                    metric.Service = service

                    # annotate with resource name and id derived from metric Dimensions
                    metric.ResourceName = enrich.get_metric_resource_name(metric)
                    metric.ResourceId = enrich.get_metric_resource_id(metric)

                    alarm = metric.copy()
                    del alarm.Dimensions
                    alarms[service][metric.MetricName].append(alarm)

    # temporarily save all metric data

    # metric_data = json.dumps(metrics, indent=2)
    # metric_file = open(f"{file_path}/metrics.json", "w")
    # metric_file.write(metric_data)

    # LATER allow override with monitoring options from tags

    # document alarms in json
    # alarm_data = json.dumps(alarms, indent=2)
    # alarm_file = open(f"{file_path}/alarms.json", "w")
    # alarm_file.write(alarm_data)

    # generate in tfvars format
    alarm_file = open(f"{file_path}/alarms.tfvars", "w")
    for service in alarms:
        for metric in alarms[service]:
            group = f"{service}__{metric}"
            # group_alarm_data = json.dumps(alarms[service][metric], indent=2)
            group_alarm_data = format_terraform.get_tf_list(alarms[service][metric], 2)
            alarm_file.write(f"{group} = {group_alarm_data}")


if __name__ == "__main__":

    MONITORED_REGIONS = ["eu-west-1", "eu-west-2", "us-east-1"]

    # Match boto3 casing for consistency
    METRIC_RULES = [
        Dict({
            "Namespace": "AWS/SQS",
            "MetricName": "ApproximateAgeOfOldestMessage",
            "Statistic": "Maximum",
            "Multiplier": 1.1,
            "Minimum": 300,
            "Maximum": (4 * 24 * 60 * 60)
        })
    ]
    main()
