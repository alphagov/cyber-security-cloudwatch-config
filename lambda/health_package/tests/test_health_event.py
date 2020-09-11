"""Test HealthEvent class """
import json
from datetime import datetime

import pytest

from ..health_event import HealthEvent


@pytest.mark.usefixtures("event_args")
def test_event_populate(event_args):
    """
    Test populate method correctly assigns object attributes
    """

    event = HealthEvent()
    event.populate(**event_args)

    assert event.source == event_args.get("source")
    assert event.component_type == event_args.get("component_type")
    assert event.event_type == event_args.get("event_type")
    assert event.environment == event_args.get("environment")
    assert event.service == event_args.get("service")
    assert event.healthy == event_args.get("healthy")
    assert event.resource["Name"] == event_args.get("resource_name")
    # assert event.resource["ID"] == event_args.get("None")
    assert event.source_data == event_args.get("source_data")
    assert event.metric_data == event_args.get("metric_data")


@pytest.mark.usefixtures("event_args")
def test_to_json(event_args):
    """
    Test to_json method correctly converts object instance to JSON
    """

    event = HealthEvent()
    event.populate(**event_args)
    now = datetime.utcnow()
    event.metric_data[0]["Timestamp"] = now
    json_event = event.to_json()
    event_dictionary = json.loads(json_event)

    assert event_dictionary["Source"] == event_args.get("source")
    assert event_dictionary["ComponentType"] == event_args.get("component_type")
    assert event_dictionary["EventType"] == event_args.get("event_type")
    assert event_dictionary["Environment"] == event_args.get("environment")
    assert event_dictionary["Service"] == event_args.get("service")
    assert event_dictionary["Healthy"] == event_args.get("healthy")
    assert event_dictionary["Resource"]["Name"] == event_args.get("resource_name")
    # this assert also checks that field_1 in the sourcedata is still snake case
    assert event_dictionary["SourceData"] == event_args.get("source_data")

    timestamp = event_dictionary.get("MetricData")[0]["Timestamp"]
    assert datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") == now


def test_set_resource():
    """
    Test resource name and id handling
    """

    event = HealthEvent()
    resource_name = "a test resource name"
    event.set_resource(resource_name=resource_name)

    assert event.resource["Name"] == resource_name
    assert event.resource["ID"] is None

    event = HealthEvent()
    resource_id = "a test resource ID"
    event.set_resource(resource_id=resource_id)

    assert event.resource["ID"] == resource_id
    assert event.resource["Name"] is None
