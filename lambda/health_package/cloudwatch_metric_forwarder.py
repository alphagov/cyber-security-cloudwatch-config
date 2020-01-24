"""
Entrypoint for scheduled cloudwatch metrics forwarding
"""
import json
from datetime import datetime
from collections import defaultdict

from addict import Dict
import boto3

from logger import LOG
import enrich
from cloudwatch_forwarder import (
    get_standard_health_event_template,
    send_to_health_monitor
)


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
            metric_event = cloudwatch_metric_to_standard_health_data_model(alarm, statistics)
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
    """ Transform data from native CloudWatch
        into a shared data model independent of the data source
    """
    session = boto3.session.Session()
    region = session.region_name
    metric = Dict()
    metric.update(alarm)
    metric.update(alarm.Dimensions)
    helper = enrich.get_namespace_helper(metric.Namespace)
    LOG.debug("Using %s helper", helper.__class__.__name__)
    tags = helper.get_tags_for_metric_resource(
        metric,
        region=region
    )
    alarm.Tags = tags
    LOG.debug("Tags: %s", json.dumps(tags))

    event = get_standard_health_event_template()
    event.Source = "AWS/CloudWatch"
    event.EventType = "Metric"
    event.NotifySlack = False
    event.Environment = tags.get("Environment", "Test").lower()
    event.Service = tags.get("Service", "Unknown")
    event.Healthy = (alarm.StateValue == "OK")
    event.ComponentType = alarm.Namespace
    event.Resource.Name = helper.get_metric_resource_name(metric)
    event.Resource.ID = helper.get_metric_resource_id(metric)
    event.SourceData = alarm
    event.MetricData = metric_data

    if metric_data is not None:
        event.MetricData = metric_data

    LOG.debug("Standardised event: %s", json.dumps(event, default=str))
    return event


def main():
    """
    Test running the function in script mode
    """
    process_cloudwatch_metric_event()


if __name__ == "__main__":
    main()
