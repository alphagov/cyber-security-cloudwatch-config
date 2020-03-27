""" Test LambdaHelper class"""
import pytest

from components.lambda_helper import LambdaHelper
import stubs


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
    """ Check that we can resolve the metric resource
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


@pytest.mark.usefixtures("lambda_metric")
@pytest.mark.usefixtures("mock_get_function_response")
@pytest.mark.usefixtures("mock_list_tags_response")
@pytest.mark.usefixtures("metric_rule")
def test_get_metric_threshold(
    mock_get_function_response, mock_list_tags_response, metric_rule, lambda_metric
):
    """Test get_metric_threshold subclass method"""
    stubber = stubs.mock_lambda(mock_get_function_response, mock_list_tags_response)

    with stubber:
        helper = LambdaHelper()
        threshold = helper.get_metric_threshold(lambda_metric, metric_rule)
        assert threshold.Maximum == 200
        assert threshold.Minimum == 3
        assert threshold.Configuration.Timeout == 60
