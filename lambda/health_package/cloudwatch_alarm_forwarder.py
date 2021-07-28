"""
Entrypoint for processing a cloudwatch alarm event from SNS
"""
import json

import boto3

import enrich
from cloudwatch_forwarder import parse_sns_message, send_to_health_monitor
from health_event import HealthEvent
from logger import LOG


def process_cloudwatch_alarm_event(event):
    """ Receive raw event from lambda invoke """
    message = parse_sns_message(event)
    standardised_data = cloudwatch_alarm_to_standard_health_data_model(message)
    response = send_to_health_monitor(standardised_data)
    LOG.debug("Lambda invoke status: %s", response.StatusCode)
    return response.StatusCode == 200


def cloudwatch_alarm_to_standard_health_data_model(source_message):
    """Transform data from native CloudWatch
    into a shared data model independent of the data source
    """
    metric = source_message.Trigger
    helper = enrich.get_namespace_helper(metric.Namespace)
    source_message.Tags = helper.get_tags_for_metric_resource(metric)

    event = HealthEvent()

    resource_name = helper.get_metric_resource_name(metric)
    resource_id = helper.get_metric_resource_id(metric)
    session = boto3.session.Session()
    region = session.region_name
    account_id = session.client("sts").get_caller_identity().get("Account")
    new_state_healthy = source_message.NewStateValue == "OK"
    old_state_insufficient = source_message.OldStateValue == "INSUFFICIENT_DATA"
    # Suppress sending to Slack when going from INSUFFICIENT_DATA to OK
    # When new alarms are created or updated and go back to healthy
    # we don't really need to see that in Slack
    notify_slack = not (new_state_healthy and old_state_insufficient)

    event.populate(
        source="aws.cloudwatch",
        component_type=source_message.Trigger.Namespace,
        event_type="Alarm",
        environment=source_message.Tags.get("Environment", "Test").lower(),
        service=source_message.Tags.get("Service", "Unknown"),
        healthy=new_state_healthy,
        notify_slack=notify_slack,
        resource_name=resource_name,
        resource_id=resource_id,
        source_data=source_message,
        aws_account_id=account_id,
        aws_region=region,
    )

    LOG.debug("Standardised event: %s", json.dumps(event, default=str))
    return event
