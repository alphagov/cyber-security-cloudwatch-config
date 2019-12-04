""" Process an alarm from CloudWatch """
import os
import json
import logging
import base64

import boto3
from addict import Dict

import enrich

LOG = logging.getLogger()
LOG.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG")))


def process_cloudwatch_event(event):
    """ Receive raw event from lambda invoke """
    message = parse_sns_message(event)
    standardised_data = cloudwatch_to_standard_health_data_model(message)
    response = send_to_health_monitor(standardised_data)
    return response.StatusCode == 200


def get_caller_identity():
    """ Get a session for the IAM role to invoke the health lambda """
    aws_sts = boto3.client("sts")
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
    aws_sts = boto3.client("sts")
    account_id = get_environment_account_id(environment)
    role_name = os.environ.get("TARGET_ROLE")
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    role_session_name = f"{role_name}_{account_id}"
    session = aws_sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )
    return session


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

    payload_json = json.dumps(message)
    payload_bytes = payload_json.encode('utf-8')
    context = get_client_context()

    aws_lambda = boto3.client(
        "lambda",
        aws_access_key_id=session["AccessKeyId"],
        aws_secret_access_key=session["SecretAccessKey"],
        aws_session_token=session["SessionToken"],
        region_name=target_region,
    )

    invoke_params = {
        "FunctionName": lambda_function,
        "InvocationType": 'Event',
        "ClientContext": context,
        "Payload": payload_bytes
    }
    LOG.debug("Invoke arguments: %s", json.dumps(invoke_params))
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
        "Service": "Unknown",
        "Healthy": True,
        "ComponentType": "",
        "Resource": {
            "Name": "",
            "ID": ""
        },
        "SourceData": {}
    })


def cloudwatch_to_standard_health_data_model(source_message):
    """ Transform data from native CloudWatch
        into a shared data model independent of the data source
    """
    metric = source_message.Trigger
    helper = enrich.get_namespace_helper(metric.Namespace)
    source_message.Tags = helper.get_tags_for_metric_resource(metric)

    event = get_standard_health_event_template()
    event.Source = "AWS/CloudWatch"
    event.Environment = source_message.Tags.get("Environment", "Test")
    event.Service = source_message.Tags.get("Service", "Unknown")
    event.Healthy = (source_message.NewStateValue == "OK")
    event.ComponentType = source_message.Trigger.Namespace
    event.Resource.Name = helper.get_metric_resource_name(source_message.Trigger)
    event.Resource.ID = helper.get_metric_resource_id(source_message.Trigger)
    event.SourceData = source_message
    LOG.debug("Standardised event: %s", json.dumps(event))
    return event
