"""Test set alarm state"""
import boto3
# from Addict import Dict 

alarm_name = 'health-monitoring-test-alarm-2'
#alarm_name = Dict()
region = 'eu-west-2'

client = boto3.client('cloudwatch',region_name=region)

""" Get current state """
def get_alarm_state(alarm_name):

	describe_response = client.describe_alarms(
		AlarmNames=[alarm_name]
	)

	for alarm in describe_response["MetricAlarms"]:
		""" Set alarm state from Alarm to OK """
		if alarm["StateValue"] == "ALARM":
			print(f"Alarm for {str(alarm_name)} is currently set to {alarm['StateValue']}")
			set_alarm_state('OK', str(alarm_name))
			print(f"Setting state from ALARM -> OK")
		elif alarm["StateValue"] == "OK":
			""" Set alarm state from OK to ALARM """
			print(f"Alarm for {alarm_name} is currently set to {alarm['StateValue']}")
			set_alarm_state('ALARM', str(alarm_name))
			print(f"Setting state from OK -> ALARM")
		else:
			""" INSUFFICENT_DATA state """
			print(f"Alarm state for {alarm_name} is set to {alarm['StateValue']}")
			pass

""" Set alarm state """
def set_alarm_state(state, alarm_name):
	alarm_set_response = client.set_alarm_state(
		AlarmName=str(alarm_name),
		StateValue=str(state),
		StateReason='testing set alarm state'
	)
			
if __name__ == "__main__":
	get_alarm_state(alarm_name)
