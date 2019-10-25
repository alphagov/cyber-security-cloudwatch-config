import pytest


@pytest.fixture()
def lambda_event():
    """Create a request event"""
    event_data = {
        'requestContext': {
            'elb': {
                'targetGroupArn':
                'arn:aws:elasticloadbalancing:eu:1234:targetgroup/test/1234'
            }
        },
        'httpMethod': 'POST',
        'path': '/',
        'queryStringParameters': {},
        'headers': {
            'accept-encoding': 'identity',
            'connection': 'close',
            'content-length': '694',
            'content-type': 'application/json',
            'host': 'alert-controller.demo.cyber.digital',
            'user-agent': 'Splunk/ABCD1234',
            'x-amzn-trace-id': 'Root=1-1234',
            'x-forwarded-for': '1.2.3.4',
            'x-forwarded-port': '443',
            'x-forwarded-proto': 'https'
        },
        'body': '{}',
        'isBase64Encoded': False
    }

    return event_data


@pytest.fixture()
def list_metric_response():
    """Create a request event"""
    response = {
        "Metrics": [
            {
                "Namespace": "AWS/Lambda",
                "MetricName": "Throttles",
                "Dimensions": [
                    {
                        "Name": "FunctionName",
                        "Value": "csw-uat"
                    },
                    {
                        "Name": "Resource",
                        "Value": "csw-uat"
                    }
                ]
            },
            {
                "Namespace": "AWS/Lambda",
                "MetricName": "Invocations",
                "Dimensions": [
                    {
                        "Name": "FunctionName",
                        "Value": "csw-uat"
                    },
                    {
                        "Name": "Resource",
                        "Value": "csw-uat"
                    }
                ]
            },
            {
                "Namespace": "AWS/Lambda",
                "MetricName": "Errors",
                "Dimensions": [
                    {
                        "Name": "FunctionName",
                        "Value": "csw-uat"
                    },
                    {
                        "Name": "Resource",
                        "Value": "csw-uat"
                    }
                ]
            },
            {
                "Namespace": "AWS/Lambda",
                "MetricName": "Duration",
                "Dimensions": [
                    {
                        "Name": "FunctionName",
                        "Value": "csw-uat"
                    },
                    {
                        "Name": "Resource",
                        "Value": "csw-uat"
                    }
                ]
            },
            {
                "Namespace": "AWS/SQS",
                "MetricName": "ApproximateNumberOfMessagesVisible",
                "Dimensions": [
                    {
                        "Name": "QueueName",
                        "Value": "csw-dan-audit-account-metric-queue"
                    }
                ]
            },
            {
                "Namespace": "AWS/SQS",
                "MetricName": "ApproximateNumberOfMessagesDelayed",
                "Dimensions": [
                    {
                        "Name": "QueueName",
                        "Value": "csw-uat-evaluated-metric-queue"
                    }
                ]
            },
            {
                "Namespace": "AWS/SQS",
                "MetricName": "ApproximateAgeOfOldestMessage",
                "Dimensions": [
                    {
                        "Name": "QueueName",
                        "Value": "csw-dan-audit-account-queue"
                    }
                ]
            },
            {
                "Namespace": "AWS/SQS",
                "MetricName": "ApproximateNumberOfMessagesNotVisible",
                "Dimensions": [
                    {
                        "Name": "QueueName",
                        "Value": "csw-uat-evaluated-metric-queue"
                    }
                ]
            },
            {
                "Namespace": "AWS/SQS",
                "MetricName": "NumberOfMessagesSent",
                "Dimensions": [
                    {
                        "Name": "QueueName",
                        "Value": "csw-dan-evaluated-metric-queue"
                    }
                ]
            },
            {
                "Namespace": "AWS/SQS",
                "MetricName": "NumberOfMessagesDeleted",
                "Dimensions": [
                    {
                        "Name": "QueueName",
                        "Value": "csw-dan-completed-audit-queue"
                    }
                ]
            },
            {
                "Namespace": "AWS/SQS",
                "MetricName": "NumberOfEmptyReceives",
                "Dimensions": [
                    {
                        "Name": "QueueName",
                        "Value": "csw-uat-audit-account-queue"
                    }
                ]
            }
        ]
    }

    return response


