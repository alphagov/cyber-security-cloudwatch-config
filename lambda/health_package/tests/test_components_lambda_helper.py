""" Test LambdaHelper class"""
import pytest

import boto3
from botocore.stub import Stubber

from components.lambda_helper import LambdaHelper


@pytest.mark.usefixtures("lambda_metric")
@pytest.mark.usefixtures("mock_get_function_response")
@pytest.mark.usefixtures("mock_list_tags_response")
def test_metric_resource_exists(lambda_metric,
                                mock_get_function_response):
    """ Test the metric_resource_exists method """
    region = "eu-west-2"
    client = boto3.client('lambda', region_name=region)

    stubber = Stubber(client)

    # mock get_function response
    get_function_params = {
        "FunctionName": "lambda-function"
    }
    stubber.add_response('get_function', mock_get_function_response, get_function_params)

    stubber.activate()

    # override boto.client to return the mock client
    boto3.client = lambda service, region_name: client

    with stubber:
        helper = LambdaHelper()
        resource_exists = helper.metric_resource_exists(lambda_metric)
        assert resource_exists


@pytest.mark.usefixtures("lambda_metric")
@pytest.mark.usefixtures("mock_get_function_response")
@pytest.mark.usefixtures("mock_list_tags_response")
def test_get_tags_for_metric_resource(lambda_metric,
                                      mock_get_function_response,
                                      mock_list_tags_response):
    """ Check that we can resolve the metric resource
        and from that get the tags linked to that resource
    """
    region = "eu-west-2"
    client = boto3.client('lambda', region_name=region)

    stubber = Stubber(client)

    # mock get_function response
    get_function_params = {
        "FunctionName": "lambda-function"
    }
    stubber.add_response('get_function', mock_get_function_response, get_function_params)

    # mock the list_tags response
    list_tags_params = {
        "Resource": "arn:aws:lambda:eu-west-2:123456789012:function:lambda-function"
    }
    stubber.add_response('list_tags', mock_list_tags_response, list_tags_params)
    stubber.activate()

    # override boto.client to return the mock client
    boto3.client = lambda service, region_name: client

    with stubber:
        helper = LambdaHelper()
        tags = helper.get_tags_for_metric_resource(lambda_metric)
        print(str(tags))
        assert tags.Environment == "test"
        assert tags.SvcCodeURL == "https://github.com/alphagov/my-madeup-repo"
        assert tags.Name == "lambda-function"
