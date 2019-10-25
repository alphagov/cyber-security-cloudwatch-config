"""Query AWS for context about cloudwatch metric resources"""
import json

import boto3
from addict import Dict


def get_client_from_namespace(namespace, region):
    """Convert cloudwatch metric namespace to a boto3 client"""
    clients = {
        "AWS/SQS": "sqs",
        "AWS/Lambda": "lambda"
    }
    if namespace in clients:
        client_name = clients[namespace]
        client = boto3.client(client_name, region_name=region)
    else:
        client = None
    return client


def get_metric_dimension_value(metric, dimension_name):
    """Iterate metric dimensions for value of named dimension"""
    dimension_value = None
    for dim in metric.Dimensions:
        if dim.Name == dimension_name:
            dimension_value = dim.Value

    return dimension_value


def get_tags_for_metric_resource(metric, region=None):
    """
    Get QueueUrl from queue name and then get the tags if present
    """
    namespace = metric.Namespace
    tags = None
    try:
        client = get_client_from_namespace(namespace, region)
        if client:
            if namespace == "AWS/SQS":
                queue = get_metric_dimension_value(metric, "QueueName")
                print(f"Get tags for sqs queue: {queue}")
                get_url_response = Dict(client.get_queue_url(QueueName=queue))
                get_tags_response = Dict(client.list_queue_tags(QueueUrl=get_url_response.QueueUrl))
                print(json.dumps(get_tags_response.Tags, indent=2))
                tags = get_tags_response.Tags

            elif namespace == "AWS/Lambda":
                function_name = get_metric_dimension_value(metric, "FunctionName")
                if function_name:
                    print(f"Get tags for lambda function: {function_name}")
                    get_function_response = Dict(client.get_function(FunctionName=function_name))
                    lambda_arn = get_function_response.Configuration.FunctionArn
                    get_tags_response = Dict(client.list_tags(Resource=lambda_arn))
                    tags = get_tags_response.Tags
    except AttributeError as err:
        print(json.dumps(metric, indent=2))
        print(str(err))
    return tags
