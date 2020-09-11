""" Test LambdaHelper class"""
import pytest

from ..components.lambda_helper import LambdaHelper
from . import stubs


@pytest.mark.usefixtures("lambda_metric")
@pytest.mark.usefixtures("mock_get_function_response")
@pytest.mark.usefixtures("mock_list_tags_response")
def test_metric_resource_exists(
    lambda_metric, mock_get_function_response, mock_list_tags_response
):
    """ Test the metric_resource_exists method """
    stubber = stubs.mock_lambda(mock_get_function_response, mock_list_tags_response)

    with stubber:
        helper = LambdaHelper()
        resource_exists = helper.metric_resource_exists(lambda_metric)
        assert resource_exists


@pytest.mark.usefixtures("lambda_metric")
@pytest.mark.usefixtures("mock_get_function_response")
@pytest.mark.usefixtures("mock_list_tags_response")
def test_get_tags_for_metric_resource(
    lambda_metric, mock_get_function_response, mock_list_tags_response
):
    """Check that we can resolve the metric resource
    and from that get the tags linked to that resource
    """
    stubber = stubs.mock_lambda(mock_get_function_response, mock_list_tags_response)

    with stubber:
        helper = LambdaHelper()
        tags = helper.get_tags_for_metric_resource(lambda_metric)
        print(str(tags))
        assert tags.Environment == "test"
        assert tags.SvcCodeURL == "https://github.com/alphagov/my-madeup-repo"
        assert tags.Name == "lambda-function"
