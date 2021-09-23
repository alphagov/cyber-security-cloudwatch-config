""" Read cloudwatch list-metrics and generate alarm config """
import json
import os
from collections import defaultdict

import boto3
from addict import Dict
from botocore.exceptions import ClientError

import enrich
import format_terraform
from local_exceptions import ServerError
from logger import LOG


MONITORED_REGIONS = ["eu-west-1", "eu-west-2", "us-east-1"]


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
    unmonitored_resources = []

    # implement standard monitoring rules based on namespace
    for metric in METRIC_RULES:
        metric_rule = Dict(metric)
        namespace = metric_rule.Namespace
        helper = enrich.get_namespace_helper(namespace)
        service = helper.get_namespace_service(namespace)

        # print(str(metric_rule))
        for region in metrics:
            print(f"Analysing metrics for {region}\n")
            region_metrics = metrics[region]
            namespace_metrics = region_metrics[namespace]
            print(
                f"Found {len(namespace_metrics)} metrics for {namespace} in {region}\n"
            )

            if region in MONITORED_REGIONS:
                if region not in alarms:
                    alarms[region] = []

                for metric in namespace_metrics:
                    print(f"Checking rules for {metric.MetricName}")
                    if (
                        metric.MetricName == metric_rule.MetricName
                        and helper.metric_resource_exists(metric)
                    ):
                        # get metric-statistics and calculate health threshold
                        metric.Threshold = helper.get_metric_threshold(metric, metric_rule)
                        print(f"Threshold is: {metric.Threshold}")

                        # annotate with service
                        metric.Service = service

                        # annotate with resource name and id derived from metric Dimensions
                        metric.ResourceName = helper.get_metric_resource_name(metric)
                        metric.ResourceId = helper.get_metric_resource_id(metric)

                        alarm = metric.copy()
                        # print(json.dumps(alarm.Dimensions, indent=2))
                        # exit()
                        dimension = alarm.Dimensions[0]
                        alarm[f"DimensionName"] = dimension["Name"]
                        alarm[f"DimensionValue"] = dimension["Value"]
                        del alarm.Dimensions
                        alarms[region].append(alarm)
            else:
                # Log any metrics with Dimensions in unmonitored regions
                # Metrics without dimensions aren't attached to a resource
                unmonitored_region_resources = [
                    metric
                    for metric
                    in namespace_metrics
                    if len(metric.Dimensions) > 0
                ]
                if len(unmonitored_region_resources) > 0:
                    unmonitored_resources.extend(unmonitored_region_resources)

    if len(unmonitored_resources) > 0:
        print(
            f"Resources deployed into UNMONITORED REGIONS"
        )
        print(json.dumps(unmonitored_resources, indent=2))
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
        region_alarms = format_terraform.get_tf_list(
            alarms[region], 2
        )
        alarm_file.write(f"{region}_alarms = {region_alarms}")
        print(f"{region}_alarms = {region_alarms}")


if __name__ == "__main__":

    with open("metric-settings.json", "r") as metrics_file:
        METRIC_RULES = json.load(metrics_file)
        main()
