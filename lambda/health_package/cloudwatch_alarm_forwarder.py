"""
Entrypoint for processing a cloudwatch alarm event from SNS
"""
import json
import boto3

from logger import LOG
import enrich
from cloudwatch_forwarder import (
    parse_sns_message,
    get_standard_health_event_template,
    send_to_health_monitor
)


def process_cloudwatch_alarm_event(event):
    """ Receive raw event from lambda invoke """
    message = parse_sns_message(event)
    standardised_data = cloudwatch_alarm_to_standard_health_data_model(message)
    response = send_to_health_monitor(standardised_data)
    LOG.debug("Lambda invoke status: %s", response.StatusCode)
    return response.StatusCode == 200


def cloudwatch_alarm_to_standard_health_data_model(source_message):
    """ Transform data from native CloudWatch
        into a shared data model independent of the data source
    """
    session = boto3.session.Session()
    region = session.region_name
    metric = source_message.Trigger
    helper = enrich.get_namespace_helper(metric.Namespace)
    source_message.Tags = helper.get_tags_for_metric_resource(
        metric,
        region=region
    )

    event = get_standard_health_event_template()
    event.Source = "AWS/CloudWatch"
    event.EventType = "Alarm"
    event.Environment = source_message.Tags.get("Environment", "Test").lower()
    event.Service = source_message.Tags.get("Service", "Unknown")
    event.Healthy = (source_message.NewStateValue == "OK")
    event.ComponentType = source_message.Trigger.Namespace
    event.Resource.Name = helper.get_metric_resource_name(source_message.Trigger)
    event.Resource.ID = helper.get_metric_resource_id(source_message.Trigger)
    event.SourceData = source_message

    LOG.debug("Standardised event: %s", json.dumps(event))
    return event
