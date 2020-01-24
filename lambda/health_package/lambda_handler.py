"""Handler."""
from generate_metric_alarms import process_generate_metric_alarms_event
from health_monitor_lambda import process_health_event
from cloudwatch_alarm_forwarder import process_cloudwatch_alarm_event
from cloudwatch_metric_forwarder import process_cloudwatch_metric_event
from splunk_forwarder import process_update_dashboard_event
from logger import LOG


def generate_metric_alarms_handler(event, context):
    """ Lambda entrypoint for generate metric alarms script """
    LOG.info("Generate metric alarms event: %s", str(event))
    return process_generate_metric_alarms_event(event)


def health_monitor_handler(event, context):
    """ Lambda entrypoint for health monitor SNS event """
    LOG.info("Health monitor event: %s", str(event))
    process_health_event(event)


def cloudwatch_alarm_event_handler(event, context):
    """ Lambda entrypoint for cloudwatch alarm event """
    LOG.info("Cloudwatch alarm event: %s", str(event))
    process_cloudwatch_alarm_event(event)


def cloudwatch_metric_event_handler(event, context):
    """ Lambda entrypoint for cloudwatch alarm event """
    LOG.info("Cloudwatch metric event: %s", str(event))
    process_cloudwatch_metric_event()


def splunk_forwarder_event_handler(event, context):
    """ Receive and process Health Monitoring message """
    try:
        process_update_dashboard_event(event)

    except (ValueError, KeyError):
        LOG.error('Failed to build Splunk payload for health monitoring data')
