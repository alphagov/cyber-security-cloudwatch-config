""" Create mock boto3 clients for testing """
import boto3
from botocore.stub import Stubber


def _keep_it_real():
    """ Keep the native """
    if not getattr(boto3, "real_client", None):
        boto3.real_client = boto3.client


def mock_sqs(queue_url, event, mock_sqs_send_message_response):
    """ Mock SQS send message  """
    _keep_it_real()
    client = boto3.real_client('sqs')

    stubber = Stubber(client)

    event_json = event.to_json()

    function_params = {
        "QueueUrl": queue_url,
        "MessageBody": event_json
    }
    stubber.add_response('send_message', mock_sqs_send_message_response, function_params)

    stubber.activate()
    # override boto.client to return the mock client
    boto3.client = lambda service, region_name: client
    return stubber


def mock_lambda(mock_get_function_response, mock_list_tags_response):
    """ Mock lambda get function and list tags """
    _keep_it_real()
    region = "eu-west-2"

    client = boto3.real_client('lambda', region_name=region)

    stubber = Stubber(client)

    # mock get_function response
    get_function_params = {
        "FunctionName": "lambda-function"
    }
    stubber.add_response('get_function', mock_get_function_response, get_function_params)

    list_tags_params = {
        "Resource": "arn:aws:lambda:eu-west-2:123456789012:function:lambda-function"
    }
    stubber.add_response('list_tags', mock_list_tags_response, list_tags_params)

    stubber.activate()

    # override boto.client to return the mock client
    boto3.client = lambda service, region_name: client
    return stubber
