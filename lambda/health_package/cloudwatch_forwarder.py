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


def get_environment(message):
    """ Get environment from resource tags or default to DEF_ENVIRONMENT var """
    if "Environment" in message:
        environment = message.Environment
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


def assume_forwarder_role(environment):
    """ Get a session for the IAM role to invoke the health lambda """
    session = boto3.session.Session()
    region = session.region_name
    aws_sts = boto3.client("sts", region_name=region)
    account_id = get_environment_account_id(environment)
    role_name = os.environ.get("TARGET_ROLE")
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    role_session_name = f"{role_name}_{account_id}"
    session = aws_sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )
    LOG.debug("Role assumed: %s", session["Credentials"]["AccessKeyId"])
    return session["Credentials"]


def get_health_target_lambda(environment):
    """ Return production instance for matching environments or staging otherwise """
    account_id = get_environment_account_id(environment)
    target_region = os.environ.get("TARGET_REGION")
    target_lambda = os.environ.get("TARGET_LAMBDA")
    lambda_arn = f"arn:aws:lambda:{target_region}:{account_id}:function:{target_lambda}"
    return lambda_arn


def send_to_health_monitor(message):
    """ Us boto3 to invoke lamdba x-region """
    env = get_environment(message)
    session = assume_forwarder_role(env)
    # lambda_arn = get_health_target_lambda(env)
    lambda_function = os.environ.get("TARGET_LAMBDA")
    target_region = os.environ.get("TARGET_REGION")

    LOG.debug("Sending to %s in %s", lambda_function, target_region)

    payload_json = json.dumps(message, default=str)
    payload_bytes = payload_json.encode('utf-8')
    context = get_client_context()

    LOG.debug("Built payload, getting assumed role lambda client")

    aws_lambda = boto3.client(
        "lambda",
        aws_access_key_id=session["AccessKeyId"],
        aws_secret_access_key=session["SecretAccessKey"],
        aws_session_token=session["SessionToken"],
        region_name=target_region,
    )

    LOG.debug("Obtained lambda client with assumed session credentials")

    invoke_params = {
        "FunctionName": lambda_function,
        "InvocationType": 'Event',
        "ClientContext": context,
        "Payload": payload_bytes
    }
    LOG.debug("Invoke arguments: %s", json.dumps(message, default=str))
    response = aws_lambda.invoke(**invoke_params)

    return Dict(response)


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


def get_standard_health_event_template():
    """ Return an empty template record to implement a
        standard health component data model
    """
    return Dict({
        "Source": "Unknown",
        "Environment": os.environ.get("DEF_ENVIRONMENT"),
        "EventType": "Alarm/Metric",
        "Service": "Unknown",
        "Healthy": True,
        "ComponentType": "",
        "Resource": {
            "Name": "",
            "ID": ""
        },
        "SourceData": {}
    })
