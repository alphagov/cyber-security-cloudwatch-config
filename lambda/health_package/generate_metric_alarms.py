""" Read cloudwatch list-metrics and generate alarm config """
import json
import os
from collections import defaultdict

from addict import Dict
import boto3
from botocore.exceptions import ClientError

from local_exceptions import ServerError
import enrich
import format_terraform
from logger import LOG


def process_generate_metric_alarms_event(event):
    """Handles a new event request
    Placeholder copied from alert_controller implementation
    """
    LOG.info(str(event))
    return create_response(200, body="Response to HealthCheck")


def create_response(status_code, status_description="", body=""):
    """Configure a response JSON object."""
    response = {"isBase64Encoded": False, "headers": {"Content-Type": "text/html;"}}

    if not status_description:
        description = {
            200: "200 OK",
            400: "400 Bad Request",
            401: "401 Unauthorized",
            405: "405 Method Not Allowed",
            500: "500 Internal Server Error",
        }
        status_description = description.get(status_code)

    response["statusCode"] = status_code
    response["statusDescription"] = status_description
    response["body"] = body

    return response


def create_sns_message(alert):
    """Create the message to publish to SNS"""
    try:
        payload = json.dumps({"alert": alert})

        message = json.dumps(
            {"default": "Default payload", "sqs": payload, "lambda": payload}
        )
        LOG.debug("MESSAGE: %s", message)

        return message
    except TypeError as err:
        raise ServerError("Error creating SNS message") from err


def publish_alert(message, topic_arn):
    """Publish alert message to SNS"""
    try:
        sns = boto3.client("sns")
        sns_response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="New report-phishing alert recorded",
            MessageStructure="json",
        )
        LOG.debug("SNS Response: %s", sns_response)
        LOG.info("Alert published to SNS")

        return sns_response
    except ClientError as err:
        raise ServerError("Error publishing message to SNS") from err


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
    """
    Get caller based on current AWS credentials
    """
    client = boto3.client("sts")
    response = Dict(client.get_caller_identity())
    return response


def get_output_file_path():
    """ Generate path to output tfvars and ensure directory exists """
    caller_response = get_caller()
    file_path = f"../../terraform/per_account/deployments/{caller_response.Account}/"
    os.makedirs(file_path, exist_ok=True)
    return file_path


def get_metric_alarms(metrics):
    """
    Iterate over metrics and return alarm config
    """
    alarms = Dict()

    # implement standard monitoring rules based on namespace
    for metric_rule in METRIC_RULES:
        namespace = metric_rule.Namespace
        helper = enrich.get_namespace_helper(namespace)
        service = helper.get_namespace_service(namespace)

        # print(str(metric_rule))
        for region in metrics:
            if region not in alarms:
                alarms[region] = defaultdict(list)
            if service not in alarms[region]:
                alarms[region][service] = defaultdict(list)

            print(f"Analysing metrics for {region}\n")
            region_metrics = metrics[region]
            namespace_metrics = region_metrics[namespace]
            print(
                f"Found {len(namespace_metrics)} metrics for {namespace} in {region}\n"
            )
            for metric in namespace_metrics:
                print(f"Checking rules for {metric.MetricName}")
                if (
                    metric.MetricName == metric_rule.MetricName
                    and helper.metric_resource_exists(metric, region=region)
                ):
                    # get metric-statistics and calculate health threshold
                    metric.Threshold = helper.get_metric_threshold(metric, metric_rule)

                    # annotate with service
                    metric.Service = service

                    # annotate with resource name and id derived from metric Dimensions
                    metric.ResourceName = helper.get_metric_resource_name(metric)
                    metric.ResourceId = helper.get_metric_resource_id(metric)

                    alarm = metric.copy()
                    del alarm.Dimensions
                    alarms[region][service][metric.MetricName].append(alarm)

    return alarms


def main():
    """
    Initial development of list-metrics processing logic
    Enrich with tags
    """
    metrics = get_region_metrics()

    alarms = get_metric_alarms(metrics)

    file_path = get_output_file_path()

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
    for region in alarms:
        for service in alarms[region]:
            for metric in alarms[region][service]:
                metric_var_name = metric.replace(".", "")
                group = f"{region}__{service}__{metric_var_name}"
                # group_alarm_data =
                #    json.dumps(alarms[region][service][metric], indent=2)
                group_alarm_data = format_terraform.get_tf_list(
                    alarms[region][service][metric], 2
                )
                alarm_file.write(f"{group} = {group_alarm_data}")


if __name__ == "__main__":

    MONITORED_REGIONS = ["eu-west-1", "eu-west-2", "us-east-1"]

    # Match boto3 casing for consistency
    # Suggested thresholds
    # sqs__NumberOfMessagesSent < 10
    # for 1 datapoints within 5 minutes
    # sqs__ApproximateAgeOfOldestMessage > 4
    # for 1 datapoints within 5 minutes
    # kinesis__PutRecordSuccess < 1
    # for 1 datapoints within 5 minutes
    # kinesis__GetRecordsIteratorAgeMilliseconds >= 43200000
    # for 1 datapoints within 1 hour
    # kinesis__GetRecordsSuccess < 1
    # for 1 datapoints within 15 minutes
    # firehose__ExecuteProcessingSuccess < 1
    # for 1 datapoints within 5 minutes
    # firehose__ExecuteProcessingDuration > 60
    # for 1 datapoints within 5 minutes
    # firehose__ThrottledGetShardIterator > 1
    # for 1 datapoints within 5 minutes
    # firehose__DeliveryToS3DataFreshness > 500
    # for 1 datapoints within 5 minutes
    METRIC_RULES = [
        Dict(
            {
                "Namespace": "AWS/SQS",
                "MetricName": "ApproximateAgeOfOldestMessage",
                "Statistic": "Maximum",
                "Multiplier": 1.1,
                "Minimum": 2,
                "Maximum": 300,  # this is an initial guess to be tuned later
            }
        ),
        Dict(
            {
                "Namespace": "AWS/SQS",
                "MetricName": "ApproximateNumberOfMessagesVisible",
                "Statistic": "Maximum",
                "Multiplier": 1.1,
                "Minimum": 500,
                "Maximum": 5000,  # this is an initial guess to be tuned later
            }
        ),
        Dict(
            {
                "Namespace": "AWS/Kinesis",
                "MetricName": "PutRecord.Success",
                "Statistic": "Minimum",
                "Multiplier": 1,
                "Minimum": 0.99,  # alert on 1% failure
            }
        ),
        Dict(
            {
                "Namespace": "AWS/Firehose",
                "MetricName": "ExecuteProcessing.Success",
                "Statistic": "Minimum",
                "Multiplier": 1,
                "Minimum": 0.99,  # alert on 1% failure
            }
        ),
        Dict(
            {
                "Namespace": "AWS/Kinesis",
                "MetricName": "GetRecords.IteratorAgeMilliseconds",
                "Statistic": "Maximum",
                "Multiplier": 1.1,
                "Minimum": 300,
                "Maximum": 43200000,  # 12 hours
            }
        ),
        Dict(
            {
                "Namespace": "AWS/Firehose",
                "MetricName": "ThrottledGetShardIterator",
                "Statistic": "Maximum",
                "Multiplier": 1.1,
                "Minimum": 2,
                "Maximum": 10,
            }
        ),
        Dict(
            {
                "Namespace": "AWS/Firehose",
                "MetricName": "KinesisMillisBehindLatest",
                "Statistic": "Maximum",
                "Multiplier": 1.1,
                "Minimum": 3000,
                # Not interested in less than 3 seconds delay
                "Maximum": 60000,
                # We'd want to know if there was a minute delay in kinesis
            }
        ),
        Dict(
            {
                "Namespace": "AWS/Lambda",
                "MetricName": "Errors",
                "Statistic": "Maximum",
                "Multiplier": 1.1,
                "Minimum": 10,
                # We probably don't want to know the first few times a lambda errors
                "Maximum": 200,
                # We definitely want to know if it errors frequently
            }
        ),
        Dict(
            {
                "Namespace": "AWS/Lambda",
                "MetricName": "Duration",
                "Statistic": "Maximum",
                "Multiplier": 1.1,
                "Minimum": 3000,
                # Any lambda running for less than 3 secs should be fine
                # The maximum is calculated based on the lambda's timeout.
                # This is measured in milliseconds (I think that has changed)
            }
        ),
    ]
    main()
