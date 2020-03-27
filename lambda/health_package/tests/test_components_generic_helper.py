""" Test GenericHelper class """
import pytest

from components.generic_helper import GenericHelper
import stubs


@pytest.mark.usefixtures("list_metric_response")
def test_get_namespace_service(list_metric_response):
    """ Test get_namespace_service classmethod """
    metric0 = list_metric_response.Metrics[0]
    helper = GenericHelper()
    service = helper.get_namespace_service(metric0.Namespace)
    assert service == "lambda"


@pytest.mark.usefixtures("dimension_metric")
def test_get_metric_dimension_value(dimension_metric):
    """ Test get_metric_dimension_value classmethod """
    instance_id = "i-0123456789abcdef0"
    helper = GenericHelper()
    dimension_value = helper.get_metric_dimension_value(dimension_metric, "InstanceId")
    assert instance_id == dimension_value


@pytest.mark.usefixtures("dimension_metric")
def test_get_metric_resource_id(dimension_metric):
    """ Test get_metric_resource_id classmethod """
    instance_id = "i-0123456789abcdef0"
    helper = GenericHelper()
    dimension_value = helper.get_metric_resource_id(dimension_metric)
    assert instance_id == dimension_value


@pytest.mark.usefixtures("dimension_metric")
def test_get_metric_resource_name(dimension_metric):
    """ Test get_metric_resource_name classmethod """
    instance_name = "instance-name"
    helper = GenericHelper()
    dimension_value = helper.get_metric_resource_name(dimension_metric)
    assert instance_name == dimension_value


@pytest.mark.usefixtures("lambda_metric")
@pytest.mark.usefixtures("mock_get_metric_statistics")
def test_get_metric_statistics(lambda_metric, mock_get_metric_statistics):
    """ Test get_metric_statistics classmethod """
    stubber = stubs.mock_cloudwatch(mock_get_metric_statistics)

    with stubber:
        helper = GenericHelper()
        statistic = "Maximum"
        lambda_values = helper.get_metric_statistics(lambda_metric, statistic)
        print(str(lambda_values))
        datapoint = lambda_values.Datapoints[0]
        assert datapoint.Timestamp == "2020-03-27T11:29:51.780Z"
        assert datapoint.Minimum == 123.0
        assert datapoint.Maximum == 123.0
        assert datapoint.Unit == "Seconds"
