"""Query AWS for context about cloudwatch metric resources"""
from components.generic_helper import GenericHelper
from components.firehose_helper import FirehoseHelper
from components.kinesis_helper import KinesisHelper
from components.lambda_helper import LambdaHelper
from components.sqs_helper import SqsHelper

# from logger import LOG


def get_namespace_helper(namespace):
    """
    Convert CloudWatch namespace
    to a component helper class instance
    """
    clients = {
        "AWS/SQS": SqsHelper,
        "AWS/Lambda": LambdaHelper,
        "AWS/Firehose": FirehoseHelper,
        "AWS/Kinesis": KinesisHelper,
    }
    ComponentHelper = clients.get(namespace, GenericHelper)

    return ComponentHelper()
