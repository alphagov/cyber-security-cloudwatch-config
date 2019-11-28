""" Mock event data for unit tests """
import json
import pytest

from addict import Dict


@pytest.fixture()
def lambda_event():
    """Create a request event"""

    alarm_data = {
        "AlarmName": "example-cloudwatch-alarm",
        "AlarmDescription": "testing state change from OK -> ALARM",
        "AWSAccountId": "123456789012",
        "NewStateValue": "ALARM",
        "NewStateReason": "Threshold Crossed: 1 out of the last 1 datapoints [1.0 (22/11/19 15:38:00)] was less than the threshold (5.0) (minimum 1 datapoint for OK -> ALARM transition).",
        "StateChangeTime": "2019-11-22T15:43:51.730+0000",
        "Region": "EU (London)",
        "OldStateValue": "OK",
        "Trigger": {
            "MetricName": "Invocations",
            "Namespace": "AWS/Lambda",
            "StatisticType": "Statistic",
            "Statistic": "AVERAGE",
            "Unit": None,
            "Dimensions": [],
            "Period": 300,
            "EvaluationPeriods": 1,
            "ComparisonOperator": "LessThanThreshold",
            "Threshold": 5.0,
            "TreatMissingData": "- TreatMissingData:                    missing",
            "EvaluateLowSampleCountPercentile": ""
        }
    }

    event_data = Dict({
        'Records': [
            {
                'EventSource': 'aws:sns',
                'EventVersion': '1.0',
                'EventSubscriptionArn': 'arn:aws:sns:eu-west-2:123456789012:health-monitoring-test-topic:3908eac2-28e6-4621-b3fe-749f20fafecc',
                'Sns': {
                    'Type': 'Notification',
                    'MessageId': '12345678-1234-5678-9012-123456789012',
                    'TopicArn': 'arn:aws:sns:eu-west-2:103495720024:health-monitoring-test-topic',
                    'Subject': 'ALARM: "example-cloudwatch-alarm" in EU (London)',
                    'Message': json.dumps(alarm_data),
                    'Timestamp': '2019-11-22T15:43:51.780Z',
                    'SignatureVersion': '1',
                    'Signature': 'oJj8Csqqzoa9Lh4LiV6O8/OVSMX6ahZ4WqcPfUuMRv2zN5NX2mBzIvGi7M+bAsc6Cs/HP7FJy9amMZBMuFfnelLG5k94Cu7NDbqMjhhoY/VMrf5QOw+5aPCl0wzKIopng+rwajGLAx2I2psbH3fgreZNYYVkNTXigPCOp9zM7WM6fzrxlA5vlOWKoFqeMKWkMYs+Te0y2FjsjsywBxc9iz/Nil7jYGNNdj5Gk3haWCuO8XCG3q+hc0MFkWWib0d858WOdAJKqqTBSrCpvieOdL+IzSCK4vbaneVr+pt39R9FN5gefDhqdQF3wBKMOSfdeBSc3v8Rn8ol4VDiptqZog==',
                    'SigningCertUrl': 'https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-123456789012abcd123456789012abcd.pem',
                    'UnsubscribeUrl': 'https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:103495720024:health-monitoring-test-topic:3908eac2-28e6-4621-b3fe-12345678abcd',
                    'MessageAttributes': {}
                }
            }
        ]
    })

    return event_data