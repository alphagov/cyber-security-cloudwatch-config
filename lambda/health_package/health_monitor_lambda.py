""" Health monitoring lambda """
import json
import os

import boto3
from addict import Dict
from logger import LOG
from cloudwatch_forwarder import parse_messages


def flatten_alarm_data_structure(message):
    """ Add trigger sub-dictionary keys to main dictionary """
    flattened_message = message.copy()
    flattened_message.update(message["Trigger"])
    return flattened_message


def process_health_event(event):
    """ Process SNS message and notify PagerDuty, Slack and dashboard """

    # If lambda is invoked via SNS
    LOG.debug("Raw event: %s", json.dumps(event))
    if "Records" in event:
        messages = parse_messages(event)
    else:
        messages = [event]

    for message in messages:
        process_health_message(message)


def process_health_message(message):
    """ Process each message from the parent invocation event """
    # These should be defined by the component type or resource tags
    # Hard-code for now
    notify_slack = message.get("NotifySlack", True)
    notify_pagerduty = False
    notify_dashboard = True

    if 'Source' and 'Resource' in message:
        if notify_pagerduty:
            notify_pagerduty_sns(message)

        if notify_slack:
            notify_slack_sns(message)

        if notify_dashboard:
            notify_dashboard_sns(message)
    else:
        LOG.debug("Message missing required fields")


def get_slack_channel(message):
    """ Identify target slack channel """
    if "AlarmName" in message:
        LOG.debug("Get target channel for alarm: %s", message['AlarmName'])
    default_channel = "cyber-security-service-health"
    # correct this to do something that might happen
    if "SlackChannel" in message:
        target_channel = message["SlackChannel"]
    else:
        target_channel = default_channel
    return target_channel


def get_resource_string(resource):
    """
    Return a string resource identifier
    depending on which fields are populated
    """
    names = []
    if "Name" in resource:
        names.append(resource["Name"])
    if "ID" in resource:
        resource_id = resource["ID"]
        names.append(f"(ID: {resource_id})")
    return " ".join(names)


def format_slack_message(message):
    """ Format message string for rendering in Slack """
    try:
        content = Dict()

        content.service = message.get("Service", "untagged")
        content.environment = message.get("Environment", "Test").title()
        content.resource = get_resource_string(message.get("Resource", {"Name": "missing"}))
        content.component_type = message.get("ComponentType", "unknown type")
        content.state = "healthy" if message.get("Healthy", False) else "unhealthy"
        content.header = f"{content.component_type}: {content.resource} is {content.state}"
        content.message = message.get("Message", None)

    except (ValueError, KeyError) as err:
        LOG.debug("Failed to read health event: %s", str(err))

    return content


def get_slack_post(message):
    """ Get channel and formatted string message as dict """

    emoji = "blue-pill" if message.get("Healthy", False) else "red-pill"
    status = "Healthy" if message.get("Healthy", False) else "Unhealthy"
    slack_post = {
        "username": f"Health Monitor: {status}",
        "icon_emoji": emoji,
        "channel": get_slack_channel(message)
    }
    content = format_slack_message(message)
    slack_post.update(content)
    return slack_post


def notify_pagerduty_sns(pagerduty_sns_message):
    """ Send message to PagerDuty SNS """
    pagerduty_sns_arn = os.environ['PAGERDUTY_SNS_ARN']
    send_to_sns(pagerduty_sns_arn, json.dumps(pagerduty_sns_message))


def notify_slack_sns(slack_sns_message):
    """ Send message to Slack SNS """
    slack_sns_arn = os.environ['SLACK_SNS_ARN']
    slack_post = get_slack_post(slack_sns_message)
    send_to_sns(slack_sns_arn, slack_post)


def notify_dashboard_sns(dashboard_sns_message):
    """ Send message to Dashboard SNS """
    dashboard_sns_arn = os.environ['DASHBOARD_SNS_ARN']
    send_to_sns(dashboard_sns_arn, json.dumps(dashboard_sns_message))


def send_to_sns(topic_arn, sns_message):
    """ Send message to SNS """
    message_to_send = json.dumps({'default': json.dumps(sns_message)})
    session = boto3.session.Session()
    region = session.region_name
    sns = boto3.client('sns', region_name=region)
    sns.publish(
        TopicArn=topic_arn,
        # Subject=sns_subject,
        Message=message_to_send,
        MessageStructure='json'
    )


if __name__ == "__main__":
    print("No run task defined yet")
