"""Test."""
import pytest

from generate_metric_alarms import process_generate_metric_alarms_event


@pytest.mark.usefixtures("lambda_event")
def test_event_healthcheck(lambda_event):
    """Test response"""
    event_healthcheck = {"headers": {}}
    event_healthcheck["headers"]["user-agent"] = "ELB-HealthChecker/2.0"
    event_healthcheck["body"] = ""

    lambda_event.update(event_healthcheck)
    response = process_generate_metric_alarms_event(lambda_event)

    assert response["statusCode"] == 200
    assert response["body"] == "Response to HealthCheck"
