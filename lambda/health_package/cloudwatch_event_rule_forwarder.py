"""
Entrypoint for processing cloudwatch event rule data from SNS
"""
import json

import boto3

import enrich
from cloudwatch_forwarder import parse_sns_message, send_to_health_monitor
from health_event import HealthEvent
from logger import LOG


def process_cloudwatch_event_rule(event):
    """ Receive raw event from lambda invoke """
    message = parse_sns_message(event)
    standardised_data = cloudwatch_event_rule_to_standard_health_data_model(message)
    response = send_to_health_monitor(standardised_data)
    LOG.debug("Lambda invoke status: %s", response.StatusCode)
    return response.StatusCode == 200


def extract_key_from_tags(tags_list, key, default):
    for tag_dict in tags_list:
        if tag_dict["key"] == key:
            return tag_dict["value"]
    return default


def cloudwatch_event_rule_to_standard_health_data_model(source_message):
    """Transform data from native CloudWatch
    into a shared data model independent of the data source
    """
    LOG.info("source_message: %s", str(source_message))
    helper = enrich.get_namespace_helper(source_message.source)
    source_message.Tags = helper.get_tags_for_metric_resource(source_message)

    event = HealthEvent()

    resource_name = source_message.detail.pipeline
    resource_id = helper.get_metric_resource_id(source_message)
    session = boto3.session.Session()
    region = session.region_name
    account_id = session.client("sts").get_caller_identity().get("Account")
    new_state_healthy = source_message.detail.state != "FAILED"
    old_state_insufficient = source_message.OldStateValue == "INSUFFICIENT_DATA"
    environment = extract_key_from_tags(source_message.Tags, "Environment", "Test")
    service = extract_key_from_tags(source_message.Tags, "Service", "Unknown")

    # Suppress sending to Slack when going from INSUFFICIENT_DATA to OK
    # When new alarms are created or updated and go back to healthy
    # we don't really need to see that in Slack
    notify_slack = not (new_state_healthy and old_state_insufficient)

    event.populate(
        source=source_message.source,
        component_type=source_message.source,
        event_type="Alarm",
        environment=environment,
        service=service,
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
