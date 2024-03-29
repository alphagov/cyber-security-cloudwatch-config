"""
Entrypoint for scheduled cloudwatch metrics forwarding
"""
import json
from collections import defaultdict
from datetime import datetime

import boto3
from addict import Dict

import enrich
from cloudwatch_forwarder import send_to_health_monitor
from health_event import HealthEvent
from logger import LOG

# This is the frequency of shipping metrics to Splunk
# If this value is changed you should also change
# local.metric_cron in
# terraform/per_account_deployable/locals.tf
# so that the cron is fired on the same frequency
PERIOD = 3600


def process_cloudwatch_metric_event():
    """ Trigger scheduled update of all configured alarm metrics """
    alarms = get_cloudwatch_alarms()

    stats = defaultdict(int)
    for alarm in alarms:
        alarm = Dict(alarm)
        current_state = alarm.StateValue
        statistics = None
        if current_state != "INSUFFICIENT_DATA":
            statistics = get_cloudwatch_metric_statistics(alarm)

        if statistics is not None:
            metric_event = cloudwatch_metric_to_standard_health_data_model(
                alarm, statistics
            )
            response = send_to_health_monitor(metric_event)
            LOG.debug("Lambda invoke status: %s", response.StatusCode)
            if response.StatusCode == 200:
                stats["sent"] += 1
            else:
                stats["failed"] += 1
        else:
            stats["no_data"] += 1
            LOG.debug("%s state is %s", alarm.MetricName, current_state)

    return stats


def get_cloudwatch_alarms():
    """ Get a list of configured cloudwatch alarms """
    aws_cloudwatch = boto3.client("cloudwatch")

    response = aws_cloudwatch.describe_alarms()
    return response["MetricAlarms"]


def get_cloudwatch_metric_statistics(alarm):
    """ Get the current metric statistics for the metric identified by an alarm """
    # print(str(alarm))
    namespace = alarm.get("Namespace")
    metric_name = alarm.get("MetricName")
    statistic = alarm.get("Statistic")
    dimensions = alarm.get("Dimensions")

    now = datetime.utcnow()
    now_timestamp = now.timestamp()
    now_offset = now_timestamp % PERIOD
    period_start = datetime.fromtimestamp(now_timestamp - now_offset - PERIOD)
    period_end = datetime.fromtimestamp(now_timestamp - now_offset)

    aws_cloudwatch = boto3.client("cloudwatch")
    response = aws_cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=period_start,
        EndTime=period_end,
        Period=PERIOD,
        Statistics=[statistic],
    )

    datapoints = response.get("Datapoints", None)

    return datapoints


def cloudwatch_metric_to_standard_health_data_model(alarm, metric_data=None):
    """Transform data from native CloudWatch
    into a shared data model independent of the data source
    """
    metric = Dict()
    metric.update(alarm)
    metric.update(alarm.Dimensions)
    helper = enrich.get_namespace_helper(metric.Namespace)
    LOG.debug("Using %s helper", helper.__class__.__name__)
    tags = helper.get_tags_for_metric_resource(metric)
    alarm.Tags = tags
    LOG.debug("Tags: %s", json.dumps(tags))

    event = HealthEvent()

    resource_name = helper.get_metric_resource_name(metric)
    resource_id = helper.get_metric_resource_id(metric)
    session = boto3.session.Session()
    region = session.region_name
    account_id = session.client("sts").get_caller_identity().get("Account")

    event.populate(
        source="aws.cloudwatch",
        component_type=alarm.Namespace,
        event_type="Metric",
        environment=tags.get("Environment", "Test").lower(),
        service=tags.get("Service", "Unknown"),
        healthy=alarm.StateValue == "OK",
        resource_name=resource_name,
        resource_id=resource_id,
        source_data=alarm,
        metric_data=metric_data,
        notify_slack=False,
        aws_account_id=account_id,
        aws_region=region,
    )

    LOG.debug("Standardised event: %s", json.dumps(event, default=str))
    return event


def main():
    """
    Test running the function in script mode
    """
    process_cloudwatch_metric_event()


if __name__ == "__main__":
    main()
