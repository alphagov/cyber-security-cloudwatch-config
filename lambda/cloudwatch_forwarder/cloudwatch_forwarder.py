""" Process an alarm from CloudWatch """
import json
import logging

from addict import Dict

from enrich import (
    get_tags_for_metric_resource,
    get_metric_resource_name,
    get_metric_resource_id
)

LOG = logging.getLogger()


def process_event(event):
    """ Receive raw event from lambda invoke """
    message = parse_sns_message(event)
    metric = message.Trigger
    message.Tags = get_tags_for_metric_resource(metric)

    return True


def parse_sns_message(event):
    """ Retrieve SNS message field from lambda invoke event """
    message = Dict(json.loads(event['Records'][0]['Sns']['Message']))

    # We don't think SNS sends multiple records in the same invocation
    # but that's an assumption so if it does we can see it happen in
    # the logs and make the case to code for it.
    if len(event['Records']) > 1:
        LOG.error("More than one record received from SNS event")
    return message


def flatten_alarm_data_structure(message):
    """ Add trigger sub-dictionary keys to main dictionary """
    flattened_message = message.copy()
    flattened_message.update(message["Trigger"])
    return flattened_message


def get_standard_health_event_template():
    """ Return an empty template record to implement a
        standard health component data model
    """
    return Dict({
        "Source": "Unknown",
        "Service": "Unknown",
        "Healthy": True,
        "ComponentType": "",
        "Resource": {
            "Name": "",
            "ID": ""
        },
        "SourceData": {}
    })


def cloudwatch_to_standard_health_data_model(source_message):
    """ Transform data from native CloudWatch
        into a shared data model independent of the data source
    """
    event = get_standard_health_event_template()
    event.Source = "AWS/CloudWatch"
    event.Service = source_message.Tags.get("Service", "Unknown")
    event.Healthy = (source_message.NewStateValue == "OK")
    event.ComponentType = source_message.Trigger.Namespace
    event.Resource.Name = get_metric_resource_name(source_message.Trigger)
    event.Resource.ID = get_metric_resource_id(source_message.Trigger)
    event.SourceData = source_message
    return event
