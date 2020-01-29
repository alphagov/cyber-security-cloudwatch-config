""" Process an alarm from CloudWatch """
import os
import json
import base64

import boto3
from addict import Dict

from logger import LOG


def get_caller_identity():
    """ Get a session for the IAM role to invoke the health lambda """
    session = boto3.session.Session()
    region = session.region_name
    aws_sts = boto3.client("sts", region_name=region)
    caller = aws_sts.get_caller_identity()
    return Dict(caller)


def get_client_context():
    """ Generate a context field for the lambda invoke """
    caller = get_caller_identity()
    b64 = base64.b64encode(caller.Arn.encode('utf-8'))
    context = f"{caller.Account}/{b64}"
    return context


def get_environment(event):
    """ Get environment from resource tags or default to DEF_ENVIRONMENT var """
    event_env = event.get_attribute("environment")
    if event_env is not None:
        environment = event_env
    else:
        environment = os.environ.get("DEF_ENVIRONMENT")

    LOG.debug("Environment: %s", environment)
    return environment


def get_environment_account_id(environment):
    """ Match production like environment names and default to test """
    prod_envs = ["live", "prod", "production"]
    account_var = "PROD_ACCOUNT" if environment.lower() in prod_envs else "TEST_ACCOUNT"
    account_id = os.environ.get(account_var)
    LOG.debug("Forward to account: %s", account_var)
    return account_id


def get_health_target_queue_url(environment):
    """ Return calculated URL for SQS target queue """
    account_id = get_environment_account_id(environment)
    target_region = os.environ.get("TARGET_REGION")
    target_queue = os.environ.get("TARGET_SQS_QUEUE")
    # https://sqs.<region>.amazonaws.com/<account>/<queue_name>
    queue_url = f"https://sqs.{target_region}.amazonaws.com/{account_id}/{target_queue}"
    return queue_url


def send_to_health_monitor(event):
    """ Us boto3 to send cross-account SQS to health monitoring environment """
    env = get_environment(event)
    target_region = os.environ.get("TARGET_REGION")
    aws_sqs = boto3.client("sqs", region_name=target_region)
    # payload_json = json.dumps(message, default=str)
    payload_json = event.to_json()
    queue_url = get_health_target_queue_url(env)
    LOG.debug("Send to SQS: %s", queue_url)
    response = aws_sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=payload_json
    )

    return Dict(response)


def get_message_body(message):
    """ Return json decoded message body from either SNS or SQS event model """
    print(str(message))
    try:
        message_text = message["body"]
        # catch addict default behaviour for missing keys
        if message_text == {}:
            raise KeyError

    except KeyError:
        message_text = message["Sns"]["Message"]

    try:
        message_body = json.loads(message_text)
    except (TypeError, json.JSONDecodeError):
        message_body = message_text

    print(str(message_body))
    return message_body


def parse_messages(event):
    """ Parse the escaped message body from each of the SQS messages in event.Records """
    messages = [
        get_message_body(record)
        for record
        in event["Records"]
    ]
    print(str(messages))
    return messages


def parse_sns_message(event):
    """ Retrieve SNS message field from lambda invoke event """
    message = Dict(json.loads(event['Records'][0]['Sns']['Message']))

    # We don't think SNS sends multiple records in the same invocation
    # but that's an assumption so if it does we can see it happen in
    # the logs and make the case to code for it.
    if len(event['Records']) > 1:
        LOG.error("More than one record received from SNS event")
    return message


def flatten_alarm_data_structure(message):
    """ Add trigger sub-dictionary keys to main dictionary """
    flattened_message = message.copy()
    flattened_message.update(message["Trigger"])
    return flattened_message
