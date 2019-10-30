import pytest

from addict import Dict


@pytest.fixture()
def lambda_event():
    """Create a request event"""
    event_data = Dict({
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
    })

    return event_data


@pytest.fixture()
def list_metric_response():
    """Create a request event"""
    response = Dict({
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
    })

    return response


@pytest.fixture()
def dimension_metric():
    metric = Dict({
        "Namespace": "AWS/EC2",
        "MetricName": "CPUUtilization",
        "Dimensions": [
            {
                "Name": "Name",
                "Value": "instance-name"
            },
            {
                "Name": "InstanceId",
                "Value": "i-0123456789abcdef0"
            }
        ]
    })

    return metric


@pytest.fixture()
def lambda_metric():
    metric = Dict({
        "Namespace": "AWS/Lambda",
        "MetricName": "Errors",
        "Dimensions": [
            {
                "Name": "FunctionName",
                "Value": "lambda-function"
            }
        ]
    })

    return metric

@pytest.fixture()
def mock_get_function_response():
    response = {
        "Configuration": {
            "FunctionName": "lambda-function",
            "FunctionArn": "arn:aws:lambda:eu-west-2:123456789012:function:lambda-function",
            "Runtime": "python3.7",
            "Role": "arn:aws:iam::103495720024:role/role_name",
            "Handler": "module.function",
            "CodeSize": 1024,
            "Description": "",
            "Timeout": 60,
            "MemorySize": 128,
            "LastModified": "2019-10-18T13:05:41.164+0000",
            "CodeSha256": "blah",
            "Version": "$LATEST",
            "VpcConfig": {
                "SubnetIds": [
                    "subnet-01234567890abcdef",
                    "subnet-11234567890abcdef",
                    "subnet-21234567890abcdef"
                ],
                "SecurityGroupIds": [
                    "sg-01234567890abcdef"
                ],
                "VpcId": "vpc-01234567890abcdef"
            },
            "Environment": {
                "Variables": {
                    "COLLECTION_NAME": "collection",
                    "DATABASE_NAME": "databasename",
                    "DATABASE_URL": "mongodb://blah",
                    "TOPIC_ARN": "arn:aws:sns:eu-west-2:123456789012:topic",
                    "LOGLEVEL": "DEBUG",
                    "VALID_TOKENS": "blah1,blah2"
                }
            },
            "TracingConfig": {
                "Mode": "PassThrough"
            },
            "RevisionId": "12345678-1234-5678-9012-123456789012"
        },
        "Code": {
            "RepositoryType": "S3",
            "Location": "https://awslambda-eu-west-2-tasks.s3.eu-west-2.amazonaws.com/snapshots/123456789012/lambda-function"
        },
        "Tags": {
            "SvcOwner": "Cyber",
            "name": "lambda-function",
            "Environment": "test",
            "Service": "cyber-service",
            "SvcCodeURL": "https://github.com/alphagov/my-madeup-repo",
            "DeployedUsing": "Terraform",
            "Name": "lambda-function"
        }
    }
    return response


@pytest.fixture()
def mock_list_tags_response():

    response = {
        "Tags": {
            "SvcOwner": "Cyber",
            "name": "lambda-function",
            "Environment": "test",
            "Service": "cyber-service",
            "SvcCodeURL": "https://github.com/alphagov/my-madeup-repo",
            "DeployedUsing": "Terraform",
            "Name": "lambda-function"
        }
    }
    return response


@pytest.fixture()
def tf_map_indent2_level0():
    map = """{
  key1 = "value1",
  key2 = "value2"
}"""
    return map


@pytest.fixture()
def tf_list_indent4_level0():
    map = """[
    "value1",
    "value2"
]"""
    return map