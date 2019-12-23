"""Test set alarm state"""
import boto3
import fire


REGIONS = ["eu-west-1", "eu-west-2"]


def get_alarms(region):
    """ Get alarm by name """

    client = boto3.client('cloudwatch', region_name=region)

    describe_response = client.describe_alarms()

    alarms = describe_response["MetricAlarms"]

    return alarms


def set_alarm_state(state, alarm_name, region):
    """ Set alarm state """
    client = boto3.client('cloudwatch', region_name=region)

    alarm_set_response = client.set_alarm_state(
        AlarmName=str(alarm_name),
        StateValue=str(state),
        StateReason='testing set alarm state'
    )
    return alarm_set_response


def reset_all_alarm_states(state):
    """
    Set state of all configured alarms to the state value
    """
    valid_states = ["OK", "ALARM"]
    if state in valid_states:
        for region in REGIONS:
            alarms = get_alarms(region)
            for alarm in alarms:
                alarm_name = alarm["AlarmName"]
                print(f"Setting {alarm_name} to {state} in {region}")
                set_alarm_state(state, alarm_name, region)

    else:
        print(
            f"State={state} is not valid. Valid values are: " +
            ", ".join(valid_states)
        )


if __name__ == "__main__":
    fire.Fire(reset_all_alarm_states)
