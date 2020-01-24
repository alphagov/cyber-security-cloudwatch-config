""" Unit tests for health monitor lambda """
import pytest

from health_monitor_lambda import (
    get_slack_channel,
    get_slack_post
)


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


@pytest.mark.usefixtures("standard_health_alarm_event")
def test_get_slack_post(standard_health_alarm_event):
    """ Test that the get slack post method returns a dictionary with the right keys """
    slack_post = get_slack_post(standard_health_alarm_event)
    assert "channel" in slack_post
    assert "state" in slack_post
