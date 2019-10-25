import pytest


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


