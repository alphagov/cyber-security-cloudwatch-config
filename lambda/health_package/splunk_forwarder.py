""" Lambda to send the Health Monitor alarm data to Splunk Cloud HEC """

import json

import boto3
import requests

from logger import LOG

SPLUNK_HEC_SSM_PARAMETER = "/health-monitoring/updated-dashboard/splunk-hec-token"
AWS_REGION = "eu-west-2"


def process_update_dashboard_event(lambda_invoke_event):
    """ Receive and process Health Monitoring message """
    try:
        LOG.debug(lambda_invoke_event)
        health_events = [
            json.loads(event["Sns"]["Message"])
            for event in lambda_invoke_event["Records"]
        ]
        for health_monitoring_message in health_events:
            LOG.info("Message: %s", str(health_monitoring_message))
            payload_to_send = build_splunk_payload(health_monitoring_message)
            send_health_monitoring_data_to_splunk(payload_to_send)

    except (ValueError, KeyError, json.JSONDecodeError) as error:
        LOG.error(
            "Failed to build Splunk payload for health monitoring data: %s", error
        )


def get_splunk_hec_token(ssm_param, region):
    """ Get Splunk Cloud HEC token from AWS SSM Parameter Store """
    ssm_client = boto3.client("ssm", region_name=region)

    try:
        ssm_response = ssm_client.get_parameter(
            Name=str(ssm_param), WithDecryption=True
        )

        return ssm_response["Parameter"]["Value"]

    except (ValueError, KeyError):

        LOG.error("Failed to retrieve Splunk Cloud HEC token")


def get_environment(health_event):
    """Get the environment setting from the source event

    Normalise to prod|test to match index names
    """
    try:
        event_env = health_event.get("Environment", "prod")
    except (TypeError):
        event_env = "prod"

    env = "prod" if event_env in ("prod", "production", "live") else "test"
    return env


def build_splunk_payload(health_monitoring_payload):
    """ Build the Health Monitoring payload to send to Splunk Cloud HEC """
    env = get_environment(health_monitoring_payload)

    payload_dictionary = {
        "index": f"cyber_services_{env}",
        "source": "health_monitoring_event",
        "sourcetype": "_json",
        "event": health_monitoring_payload,
    }

    payload_to_send = json.dumps(payload_dictionary)

    return payload_to_send


def send_health_monitoring_data_to_splunk(payload_to_send):
    """ Send the Health Monitoring payload to Splunk Cloud HEC """

    try:
        splunk_hec_token = get_splunk_hec_token(SPLUNK_HEC_SSM_PARAMETER, AWS_REGION)
        splunk_hec_endpoint = (
            "https://http-inputs-gds.splunkcloud.com/services/collector"
        )
        headers = {"Authorization": "Splunk " + splunk_hec_token}
        response = requests.post(
            splunk_hec_endpoint, payload_to_send, headers=headers, verify=False
        )

        if response.status_code != 200:
            LOG.debug("Received a non 200 HTTP status code from Splunk Cloud HEC")
            LOG.debug(
                "Response code: %s: message: %s", response.status_code, response.text
            )

        elif response.status_code == 200:
            LOG.info("Successful: message: %s", response.text)

    except (ValueError, KeyError):
        LOG.error("Failed to send health monitoring data to Splunk Cloud HEC")
