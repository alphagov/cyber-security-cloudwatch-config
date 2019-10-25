"""Test."""
import pytest

from generate_metric_alarms import process_alert


@pytest.mark.usefixtures("alert_event")
def test_event_helthcheck(alert_event):
    """Test response"""
    event_healthcheck = {'headers': {}}
    event_healthcheck['headers']['user-agent'] = 'ELB-HealthChecker/2.0'
    event_healthcheck['body'] = ''

    alert_event.update(event_healthcheck)
    response = process_alert(alert_event)

    assert response['statusCode'] == 200
    assert response['body'] == 'Response to HealthCheck'
