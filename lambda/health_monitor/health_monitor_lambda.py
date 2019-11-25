""" Health monitoring lambda """
import json
import logging
import os

import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Parse SNS message """
    LOGGER.info("Event: %s", str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    process_message(message)


def flatten_alarm_data_structure(message):
    """ Add trigger sub-dictionary keys to main dictionary """
    flattened_message = message.copy()
    flattened_message.update(message["Trigger"])
    return flattened_message


def process_message(message):
    """ Process SNS message and notify PagerDuty, Slack and dashboard """

    # These should be defined by the component type or resource tags
    # Hard-code for now
    notify_slack = True
    notify_pagerduty = False
    notify_dashboard = False

    if 'AlarmName' and 'AlarmDescription' in message:
        sns_message_to_send = flatten_alarm_data_structure(message)

        if notify_pagerduty:
            notify_pagerduty_sns(sns_message_to_send)

        if notify_slack:
            notify_slack_sns(sns_message_to_send)

        if notify_dashboard:
            notify_dashboard_sns(sns_message_to_send)
    else:
        LOGGER.debug("Message missing required fields")


def get_slack_channel(message):
    """ Identify target slack channel """
    if "AlarmName" in message:
        LOGGER.debug("Get target channel for alarm: %s", message['AlarmName'])
    default_channel = "cyber-security-service-health"
    # correct this to do something that might happen
    if "SlackChannel" in message:
        target_channel = message["SlackChannel"]
    else:
        target_channel = default_channel
    return target_channel


def format_slack_message(message):
    """ Format message string for rendering in Slack """
    namespace = message["NameSpace"]
    metric = message["MetricName"]
    alarm = message["AlarmName"]
    reason = message["NewStateReason"]
    new_state = message["NewStateValue"]
    old_state = message["OldStateValue"]
    region = message["Region"]

    slack_header = f"*{namespace} {metric} {alarm} in {region} is {new_state}"
    slack_text = f"The state changed from {old_state} for the following reason: {reason}"
    slack_message = f"{slack_header}\n\n{slack_text}"
    return slack_message


def get_slack_post(message):
    """ Get channel and formatted string message as dict """
    slack_post = {
        "channel": get_slack_channel(message),
        "message": format_slack_message(message)
    }
    return slack_post


def notify_pagerduty_sns(pagerduty_sns_message):
    """ Send message to PagerDuty SNS """
    pagerduty_sns_arn = os.environ['pagerduty_sns_arn']
    send_to_sns(pagerduty_sns_arn, json.dumps(pagerduty_sns_message))


def notify_slack_sns(slack_sns_message):
    """ Send message to Slack SNS """
    slack_sns_arn = os.environ['slack_sns_arn']
    slack_post = get_slack_post(slack_sns_message)
    send_to_sns(slack_sns_arn, json.dumps(slack_post))


def notify_dashboard_sns(dashboard_sns_message):
    """ Send message to Dashboard SNS """
    dashboard_sns_arn = os.environ['dashboard_sns_arn']
    send_to_sns(dashboard_sns_arn, json.dumps(dashboard_sns_message))


def send_to_sns(topic_arn, sns_message):
    """ Send message to SNS """
    message_to_send = json.dumps({'default': json.dumps(sns_message)})
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=topic_arn,
        # Subject=sns_subject,
        Message=message_to_send,
        MessageStructure='json'
    )


if __name__ == "__main__":
    print("No run task defined yet")
