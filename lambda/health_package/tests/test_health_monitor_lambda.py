""" Unit tests for health monitor lambda """
import pytest

from health_monitor_lambda import (
    parse_sns_message,
    get_slack_channel,
    get_slack_post
)


@pytest.mark.usefixtures("health_monitor_sns_event")
def test_parse_sns_message(health_monitor_sns_event):
    """ Test that the parse sns message correctly
    retrieves the right content from the test event """
    message = parse_sns_message(health_monitor_sns_event)
    assert "AlarmName" in message


def test_get_slack_channel():
    """ Test that get slack channel returns correct values """
    message = {}
    default_channel = "cyber-security-service-health"
    channel = get_slack_channel(message)
    assert channel == default_channel
    specified_channel = "test-specified-channel"
    message["SlackChannel"] = specified_channel
    channel = get_slack_channel(message)
    assert channel == specified_channel


@pytest.mark.usefixtures("health_monitor_sns_event")
def test_get_slack_post(health_monitor_sns_event):
    """ Test that the get slack post method returns a dictionary with the right keys """
    message = parse_sns_message(health_monitor_sns_event)
    slack_post = get_slack_post(message)
    assert "channel" in slack_post
    assert "message" in slack_post
