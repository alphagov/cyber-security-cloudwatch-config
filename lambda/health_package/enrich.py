"""Query AWS for context about cloudwatch metric resources"""
from components.codepipeline_helper import CodePipelineHelper
from components.firehose_helper import FirehoseHelper
from components.generic_helper import GenericHelper
from components.kinesis_helper import KinesisHelper
from components.lambda_helper import LambdaHelper
from components.sqs_helper import SqsHelper

# from logger import LOG


def format_namespace(namespace):
    return namespace.lower().replace("/", ".")


def get_namespace_helper(namespace):
    """
    Convert CloudWatch namespace
    to a component helper class instance
    """
    formatted_namespace = format_namespace(namespace)
    clients = {
        "aws.sqs": SqsHelper,
        "aws.lambda": LambdaHelper,
        "aws.firehose": FirehoseHelper,
        "aws.kinesis": KinesisHelper,
        "aws.codepipeline": CodePipelineHelper,
    }
    ComponentHelper = clients.get(formatted_namespace, GenericHelper)

    return ComponentHelper()
