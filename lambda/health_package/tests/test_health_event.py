"""Test HealthEvent class """
from health_event import HealthEvent


def test_event_populate():
    """
    Test populate method correctly assigns object attributes
    """

    source = "AWS/CloudWatch"
    component_type = "AWS/SQS"
    event_type = "Metric"
    environment = "MyDevEnv"
    service = "MyService"
    healthy = "OK"
    resource_name = "MyQueue"
    source_data = {
        "field_1": "value_1"
    }
    metric_data = [
        {
            "Maximum": 12.0,
            "Timestamp": "2020-01-29 09:00:00+00:00",
            "Unit": "Milliseconds"
        }
    ]

    event = HealthEvent()
    event.populate(
        source=source,
        component_type=component_type,
        event_type=event_type,
        environment="MyDevEnv",
        service=service,
        healthy=healthy,
        resource_name=resource_name,
        source_data=source_data,
        metric_data=metric_data
    )

    assert event.source == source
    assert event.component_type == component_type
    assert event.event_type == event_type
    assert event.environment == environment
    assert event.service == service
    assert event.healthy == healthy
    assert event.resource["Name"] == resource_name
    # assert event.resource["ID"] == None
    assert event.source_data == source_data
    assert event.metric_data == metric_data
