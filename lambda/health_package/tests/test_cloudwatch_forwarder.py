"""Test cloudwatch_forwarder module"""
import os

import pytest
import stubs

from cloudwatch_forwarder import (
    get_environment,
    get_environment_account_id,
    get_health_target_queue_url,
    parse_messages,
    send_to_health_monitor,
)
from health_event import HealthEvent


@pytest.mark.usefixtures("health_monitor_sns_event")
def test_parse_messages(health_monitor_sns_event):
    """Test that the parse sns message correctly
    retrieves the right content from the test event"""
    messages = parse_messages(health_monitor_sns_event)
    assert "AlarmName" in messages[0]


def test_get_environment():
    """ Test get_environment function returns based on event or default """
    os.environ["DEF_ENVIRONMENT"] = "test"

    event = HealthEvent()
    env = get_environment(event)
    assert env == "test"
    event.set_environment("prod")
    env = get_environment(event)
    assert env == "prod"


def test_get_environment_account_id():
    """ Test environment returns correct account ID """
    prod_account = "123456789012"
    test_account = "012345678901"
    os.environ["PROD_ACCOUNT"] = prod_account
    os.environ["TEST_ACCOUNT"] = test_account
    account = get_environment_account_id("test")
    assert account == test_account
    account = get_environment_account_id("Test")
    assert account == test_account
    account = get_environment_account_id("monkeys")
    assert account == test_account
    account = get_environment_account_id("live")
    assert account == prod_account
    account = get_environment_account_id("prod")
    assert account == prod_account
    account = get_environment_account_id("PROD")
    assert account == prod_account
    account = get_environment_account_id("production")
    assert account == prod_account


def test_get_health_target_queue_url():
    """ Test health queue URL generation """
    queue_name = "insert_valid_queue_name"
    region = "eu-west-2"
    os.environ["TARGET_REGION"] = region
    os.environ["TARGET_SQS_QUEUE"] = queue_name
    prod_account = "123456789012"
    test_account = "012345678901"
    os.environ["PROD_ACCOUNT"] = prod_account
    os.environ["TEST_ACCOUNT"] = test_account

    calculated_url = get_health_target_queue_url("test")
    expected_url = f"https://sqs.{region}.amazonaws.com/{test_account}/{queue_name}"
    assert calculated_url == expected_url

    calculated_url = get_health_target_queue_url("prod")
    expected_url = f"https://sqs.{region}.amazonaws.com/{prod_account}/{queue_name}"
    assert calculated_url == expected_url


@pytest.mark.usefixtures("mock_sqs_send_message_response")
def test_send_to_health_monitor(mock_sqs_send_message_response):
    """ Test send to health monitor with mock boto client """
    queue_name = "insert_valid_queue_name"
    region = "eu-west-2"
    prod_account = "123456789012"
    test_account = "012345678901"

    # Setup default environment variables
    os.environ["TARGET_REGION"] = region
    os.environ["TARGET_SQS_QUEUE"] = queue_name
    os.environ["PROD_ACCOUNT"] = prod_account
    os.environ["TEST_ACCOUNT"] = test_account

    # mock get_function response
    test_environment = "test"
    queue_url = get_health_target_queue_url(test_environment)
    event = HealthEvent()
    event.set_environment(test_environment)
    event.set_component_type("monkeys")

    stubber = stubs.mock_sqs(queue_url, event, mock_sqs_send_message_response)

    with stubber:
        response = send_to_health_monitor(event)
        assert response == mock_sqs_send_message_response
