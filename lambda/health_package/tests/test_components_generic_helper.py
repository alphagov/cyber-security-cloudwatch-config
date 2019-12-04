"""Test enrich module"""
import pytest

from components.generic_helper import GenericHelper


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
