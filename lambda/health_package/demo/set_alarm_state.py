"""Test set alarm state"""
import boto3


def get_alarm(alarm_name, region):
    """ Get alarm by name """

    client = boto3.client('cloudwatch', region_name=region)

    describe_response = client.describe_alarms(
        AlarmNames=[alarm_name]
    )

    alarm = None
    if len(describe_response["MetricAlarms"]) > 0:
        alarm = describe_response["MetricAlarms"][0]

    return alarm


def get_alarm_state(alarm_name, region):
    """ Get alarm state """
    alarm = get_alarm(alarm_name, region)

    state = None
    if alarm:
        state = alarm["StateValue"]

    return state


def set_alarm_state(state, alarm_name, region):
    """ Set alarm state """
    client = boto3.client('cloudwatch', region_name=region)

    alarm_set_response = client.set_alarm_state(
        AlarmName=str(alarm_name),
        StateValue=str(state),
        StateReason='testing set alarm state'
    )
    return alarm_set_response


def toggle_alarm_state(alarm_name, region):
    """ Toggle alarm state between OK and ALARM based on current value """

    state = get_alarm_state(alarm_name, region)

    if state is None:
        print(f"Alarm state for {alarm_name} not found")
    elif state == "ALARM":
        # Set alarm state from Alarm to OK
        print(f"Alarm for {str(alarm_name)} is currently set to {state}")
        set_alarm_state('OK', str(alarm_name), region)
        print(f"Setting state from ALARM -> OK")
    elif state == "OK":
        # Set alarm state from OK to ALARM
        print(f"Alarm for {alarm_name} is currently set to {state}")
        set_alarm_state('ALARM', str(alarm_name), region)
        print(f"Setting state from OK -> ALARM")
    else:
        # INSUFFICENT_DATA state
        print(f"Alarm state for {alarm_name} is set to {state}")


if __name__ == "__main__":
    ALARM_NAME = 'health-monitoring-test-alarm-2'
    REGION = 'eu-west-2'

    toggle_alarm_state(ALARM_NAME, REGION)
