"""Test enrich module"""
import pytest
import boto3
from botocore.stub import Stubber

import enrich


@pytest.mark.usefixtures("list_metric_response")
def test_get_namespace_service(list_metric_response):
    """ Check that the cloudwatch namespace resolves to a
        boto3 client name
    """
    metric0 = list_metric_response.Metrics[0]
    service = enrich.get_namespace_service(metric0.Namespace)
    assert service == "lambda"


@pytest.mark.usefixtures("dimension_metric")
def test_get_metric_dimension_value(dimension_metric):
    """ Check that we can retrieve a dimension by name """
    instance_id = "i-0123456789abcdef0"
    dimension_value = enrich.get_metric_dimension_value(dimension_metric, "InstanceId")
    assert instance_id == dimension_value


@pytest.mark.usefixtures("dimension_metric")
def test_get_metric_resource_id(dimension_metric):
    """ Check that we can get a dimension containing ID """
    instance_id = "i-0123456789abcdef0"
    dimension_value = enrich.get_metric_resource_id(dimension_metric)
    assert instance_id == dimension_value


@pytest.mark.usefixtures("dimension_metric")
def test_get_metric_resource_name(dimension_metric):
    """ Check that we can get a dimension matching Name """
    instance_name = "instance-name"
    dimension_value = enrich.get_metric_resource_name(dimension_metric)
    assert instance_name == dimension_value


@pytest.mark.usefixtures("lambda_metric")
@pytest.mark.usefixtures("mock_get_function_response")
@pytest.mark.usefixtures("mock_list_tags_response")
def test_get_tags_for_metric_resource(lambda_metric,
                                      mock_get_function_response,
                                      mock_list_tags_response):
    """ Check that we can resolve the metric resource
        and from that get the tags linked to that resource
    """
    client = boto3.client('lambda')

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
        tags = enrich.get_tags_for_metric_resource(lambda_metric)
        print(str(tags))
        assert tags.Environment == "test"
        assert tags.SvcCodeURL == "https://github.com/alphagov/my-madeup-repo"
        assert tags.Name == "lambda-function"
