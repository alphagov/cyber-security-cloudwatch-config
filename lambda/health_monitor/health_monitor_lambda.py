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


def process_message(message):
    """ Process SNS message and notify PagerDuty, Slack and dashboard """
    if 'AlarmName' and 'AlarmDescription' in message:
        sns_message_to_send = message.copy()
        sns_message_to_send.update(message["Trigger"])

        # notify_pagerduty_sns(json.dumps(sns_message_to_send))
        notify_slack_sns(json.dumps(sns_message_to_send))
        # notify_dashboard_sns(json.dumps(sns_message_to_send))
    else:
        LOGGER.debug("Message missing required fields")


def notify_pagerduty_sns(pagerduty_sns_message):
    """ Send message to PagerDuty SNS """
    pagerduty_sns_arn = os.environ['pagerduty_sns_arn']
    send_to_sns(pagerduty_sns_arn, pagerduty_sns_message)


def notify_slack_sns(slack_sns_message):
    """ Send message to Slack SNS """
    slack_sns_arn = os.environ['slack_sns_arn']
    send_to_sns(slack_sns_arn, slack_sns_message)


def notify_dashboard_sns(dashboard_sns_message):
    """ Send message to Dashboard SNS """
    dashboard_sns_arn = os.environ['dashboard_sns_arn']
    send_to_sns(dashboard_sns_arn, dashboard_sns_message)


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
