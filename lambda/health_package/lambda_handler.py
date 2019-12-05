"""Handler."""
import logging
import os

from generate_metric_alarms import process_generate_metric_alarms_event
from health_monitor_lambda import process_health_event
from cloudwatch_forwarder import process_cloudwatch_event

LOG = logging.getLogger()
LOG.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG")))


def generate_metric_alarms_handler(event, context):
    """ Lambda entrypoint for generate metric alarms script """
    LOG.info("Generate metric alarms event: %s", str(event))
    return process_generate_metric_alarms_event(event)


def health_monitor_handler(event, context):
    """ Lambda entrypoint for health monitor SNS event """
    LOG.info("Health monitor event: %s", str(event))
    process_health_event(event)


def cloudwatch_event_handler(event, context):
    """ Lambda entrypoint for cloudwatch alarm event """
    LOG.info("Cloudwatch event: %s", str(event))
    process_cloudwatch_event(event)
