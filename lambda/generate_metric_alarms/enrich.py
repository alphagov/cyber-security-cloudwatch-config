"""Query AWS for context about cloudwatch metric resources"""
import json
import datetime

import boto3
from addict import Dict


def get_namespace_service(namespace):
    """
    Convert CloudWatch namespace to AWS service name
    """
    client_name = None
    clients = {
        "AWS/SQS": "sqs",
        "AWS/Lambda": "lambda"
    }
    if namespace in clients:
        client_name = clients[namespace]

    return client_name


def get_client_from_namespace(namespace, region):
    """Convert cloudwatch metric namespace to a boto3 client"""
    client_name = get_namespace_service(namespace)
    if client_name:
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


def get_metric_statistics(metric, statistic):
    """
    Use get-metric-statistics to calculate appropriate alarm thresholds
    based on typical values eg maximum + 10%

    The period is calculated to match the elapsed time
    """
    # aws cloudwatch get-metric-statistics --start-time="2019-10-20T00:00:00Z" --end-time="2019-10-23T00:00:00Z"
    # --statistics=Maximum --namespace="AWS/SQS" --metric-name="ApproximateAgeOfOldestMessage"
    # --period=300 --unit=Seconds --dimensions=Name=QueueName,Value=csw-prod-audit-account-queue
    # --region=eu-west-1
    client = boto3.client("cloudwatch", metric.Region)

    x_days = 28
    now = datetime.datetime.now()
    days_ago = now - datetime.timedelta(days=x_days)
    period = 60 * 60 * 24 * x_days
    stats_response = client.get_metric_statistics(
        Namespace=metric.Namespace,
        MetricName=metric.MetricName,
        Dimensions=metric.Dimensions,
        StartTime=days_ago,
        EndTime=now,
        Period=period,
        Unit="Seconds",
        Statistics=[statistic]
    )
    return Dict(stats_response)


def get_metric_threshold(metric, rule):
    """
    Get single value of statistic and
    """
    statistic_value = None
    metric_stats = get_metric_statistics(metric, rule.Statistic)
    print(str(metric_stats))

    for datapoint in metric_stats.Datapoints:
        statistic_value = datapoint[rule.Statistic]

    threshold = statistic_value * rule.Multiplier
    if threshold < rule.Minimum:
        threshold = rule.Minimum
    elif threshold > rule.Maximum:
        threshold = rule.Maximum

    print(f"Threshold: {statistic_value} * {rule.Multiplier} = {threshold}")

    return threshold



