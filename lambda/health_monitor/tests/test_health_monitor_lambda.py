""" Unit tests for health monitor lambda """
from health_monitor_lambda import get_slack_channel


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
