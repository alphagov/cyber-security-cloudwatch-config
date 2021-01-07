"""
Entrypoint for processing a cloudwatch alarm event from SNS
"""
import json
import boto3

from logger import LOG
import enrich
from cloudwatch_forwarder import parse_sns_message, send_to_health_monitor
from health_event import HealthEvent


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
    source_message.Tags = helper.get_tags_for_metric_resource(metric, region=region)

    event = HealthEvent()

    resource_name = helper.get_metric_resource_name(metric)
    resource_id = helper.get_metric_resource_id(metric)

    event.populate(
        source="AWS/CloudWatch",
        component_type=source_message.Trigger.Namespace,
        event_type="Alarm",
        environment=source_message.Tags.get("Environment", "Test").lower(),
        service=source_message.Tags.get("Service", "Unknown"),
        healthy=source_message.NewStateValue == "OK",
        resource_name=resource_name,
        resource_id=resource_id,
        source_data=source_message,
    )

    LOG.debug("Standardised event: %s", json.dumps(event, default=str))
    return event
