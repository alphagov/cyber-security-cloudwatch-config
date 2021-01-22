""" Health monitoring lambda """
import json
import os
from collections import defaultdict

import boto3
from addict import Dict
from botocore.exceptions import ClientError

from cloudwatch_forwarder import parse_messages
from logger import LOG


def flatten_alarm_data_structure(message):
    """ Add trigger sub-dictionary keys to main dictionary """
    flattened_message = message.copy()
    flattened_message.update(message["Trigger"])
    return flattened_message


def process_health_event(event):
    """ Process SNS message and notify PagerDuty, Slack and dashboard """
    event_processed_status = defaultdict(int)
    # If lambda is invoked via SNS
    LOG.debug("Raw event: %s", json.dumps(event))
    if "Records" in event:
        messages = parse_messages(event)
    else:
        messages = [event]

    for message in messages:
        processed = process_health_message(message)
        status = "sent" if processed else "failed"
        event_processed_status[status] += 1
    return event_processed_status


def process_health_message(message):
    """ Process each message from the parent invocation event """
    # These should be defined by the component type or resource tags
    # Hard-code for now
    try:
        notify_slack = message.get("NotifySlack", True)
        notify_pagerduty = False
        notify_dashboard = True
        processed = True
        if "Source" and "Resource" in message:
            if notify_pagerduty:
                pd_response = notify_pagerduty_sns(message)
                processed = ("MessageId" in pd_response) and processed
            if notify_slack:
                slack_response = notify_slack_sns(message)
                processed = ("MessageId" in slack_response) and processed
            if notify_dashboard:
                dash_response = notify_dashboard_sns(message)
                processed = ("MessageId" in dash_response) and processed
        else:
            LOG.error("Message missing required fields")
            processed = False
    except KeyError as err:
        LOG.error("Error processing health message: %s", err)
        processed = False

    return processed


def get_slack_channel(message):
    """ Identify target slack channel """
    if "AlarmName" in message:
        LOG.debug("Get target channel for alarm: %s", message["AlarmName"])
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
        content.resource = get_resource_string(
            message.get("Resource", {"Name": "missing"})
        )
        content.component_type = message.get("ComponentType", "unknown type")
        content.state = "healthy" if message.get("Healthy", False) else "unhealthy"
        content.header = (
            f"{content.component_type}: {content.resource} is {content.state}"
        )
        content.message = message.get("Message")
        content.aws_account_id = message.get("AwsAccountId")
        content.aws_region = message.get("AwsRegion")

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
        "channel": get_slack_channel(message),
    }
    content = format_slack_message(message)
    slack_post.update(content)
    return slack_post


def notify_pagerduty_sns(pagerduty_sns_message):
    """ Send message to PagerDuty SNS """
    pagerduty_sns_arn = os.environ["PAGERDUTY_SNS_ARN"]
    response = send_to_sns(pagerduty_sns_arn, pagerduty_sns_message)
    return response


def notify_slack_sns(slack_sns_message):
    """ Send message to Slack SNS """
    slack_sns_arn = os.environ["SLACK_SNS_ARN"]
    slack_post = get_slack_post(slack_sns_message)
    response = send_to_sns(slack_sns_arn, slack_post)
    return response


def notify_dashboard_sns(dashboard_sns_message):
    """ Send message to Dashboard SNS """
    dashboard_sns_arn = os.environ["DASHBOARD_SNS_ARN"]
    response = send_to_sns(dashboard_sns_arn, dashboard_sns_message)
    return response


def send_to_sns(topic_arn, sns_message):
    """ Send message to SNS """
    try:
        message_to_send = json.dumps({"default": json.dumps(sns_message, default=str)})
        session = boto3.session.Session()
        region = session.region_name
        sns = boto3.client("sns", region_name=region)
        response = sns.publish(
            TopicArn=topic_arn,
            # Subject=sns_subject,
            Message=message_to_send,
            MessageStructure="json",
        )
    except ClientError:
        response = None
    return response


if __name__ == "__main__":
    print("No run task defined yet")
