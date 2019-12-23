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


def is_health_monitor_alarm(alarm):
    """ Check that the alarm target is the cloudwatch forwarder """
    is_health_alarm = False
    if len(alarm["OKActions"]) > 0:
        action = alarm["OKActions"][0]
        is_health_alarm = "cloudwatch_forwarder" in action
    return is_health_alarm


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
                is_health_alarm = is_health_monitor_alarm(alarm)
                if is_health_alarm:
                    print(f"Setting {alarm_name} to {state} in {region}")
                    set_alarm_state(state, alarm_name, region)
                else:
                    print(f"Not setting state: {alarm_name} is not ours")

    else:
        print(
            f"State={state} is not valid. Valid values are: " +
            ", ".join(valid_states)
        )


if __name__ == "__main__":
    fire.Fire(reset_all_alarm_states)
