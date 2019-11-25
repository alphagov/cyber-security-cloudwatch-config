""" Health monitoring lambda """
import json
import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

pagerduty_sns_arn = os.environ['pagerduty_sns_arn']
slack_sns_arn = os.environ['slack_sns_arn']
dashboard_sns_arn = os.environ['dashboard_sns_arn']

def lambda_handler(event, context):
    """ Parse SNS message """
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    process_message(message)

def process_message(message):
    """ Process SNS message and notify PagerDuty, Slack and dashboard """
    if 'AlarmName' and 'AlarmDescription' in message:
        sns_message_to_send = {
	        "AlarmName": message['AlarmName'],
			"StateChangeTime": message['StateChangeTime'],
			"OldStateValue": message['OldStateValue'],
			"NewStateValue": message['NewStateValue'],
			"NewStateReason": message['NewStateReason'],
			"Region": message['Region'],
			"AlarmDescription": message['AlarmDescription'],
			"MetricName": message['Trigger']['MetricName'],
			"NameSpace": message['Trigger']['Namespace']
		}

       	# notify_pagerduty_sns(pagerduty_sns_arn, json.dumps(sns_message_to_send))
		notify_slack_sns(slack_sns_arn, json.dumps(sns_message_to_send))
        # notify_dashboard_sns(dashboard_sns_arn, json.dumps(sns_message_to_send))
	else:
		pass
    
def notify_pagerduty_sns(pagerduty_sns_arn, pagerduty_sns_message):
	""" Send message to PagerDuty SNS """
	send_to_sns(pagerduty_sns_arn, pagerduty_sns_message)

    
def notify_slack_sns(slack_sns_arn, slack_sns_message):
	""" Send message to Slack SNS """
	send_to_sns(slack_sns_arn, slack_sns_message)

    
def notify_dashboard_sns(dashboard_sns_arn, dashboard_sns_message):
	""" Send message to Dashboard SNS """
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
