""" Lambda to send the Health Monitor alarm data to Splunk Cloud HEC """

import json
import logging
import requests
import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
SPLUNK_HEC_SSM_PARAMETER = '/health-monitoring/updated-dashboard/splunk-hec-token'
AWS_REGION = 'eu-west-2'


def lambda_handler(event, context):
    """ Receive and process Health Monitoring message """
    try:
        health_monitoring_message = json.loads(event['Records'][0]['Sns']['Message'])
        LOGGER.info("Message: " + str(health_monitoring_message))
        payload_to_send = build_splunk_payload(health_monitoring_message)
        send_health_monitoring_data_to_splunk(payload_to_send)

    except (ValueError, KeyError):
        LOGGER.exception('Failed to build Splunk payload for health monitoring data')


def get_splunk_hec_token(SPLUNK_HEC_SSM_PARAMETER, AWS_REGION):
    """ Get Splunk Cloud HEC token from AWS SSM Parameter Store """
    ssm_client = boto3.client('ssm', region_name=AWS_REGION)

    try:
        ssm_response = ssm_client.get_parameter(Name=str(SPLUNK_HEC_SSM_PARAMETER), WithDecryption=True)

        return ssm_response['Parameter']['Value']

    except (ValueError, KeyError):

        LOGGER.exception('Failed to retrieve Splunk Cloud HEC token')


def build_splunk_payload(health_monitoring_payload):
    """ Build the Health Monitoring payload to send to Splunk Cloud HEC """
    payload_dictionary = {
        "sourcetype": "_json",
        "event": health_monitoring_payload
    }

    payload_to_send = json.dumps(payload_dictionary)

    return payload_to_send


def send_health_monitoring_data_to_splunk(payload_to_send):
    """ Send the Health Monitoring payload to Splunk Cloud HEC """

    try:
        splunk_hec_token = get_splunk_hec_token(SPLUNK_HEC_SSM_PARAMETER, AWS_REGION)
        splunk_hec_endpoint = "https://http-inputs-gds.splunkcloud.com/services/collector"
        headers = {"Authorization": 'Splunk ' + splunk_hec_token}
        r = requests.post(splunk_hec_endpoint, payload_to_send, headers=headers, verify=False)

        if r.status_code != 200:
            print('Received a non 200 HTTP status code from Splunk Cloud HEC')
            print(r.status_code, r.text)
            failed = True

        elif r.status_code == 200:
            print(r.status_code, r.text)
            failed = False

    except (ValueError, KeyError):
        LOGGER.exception('Failed to send health monitoring data to Splunk Cloud HEC')
