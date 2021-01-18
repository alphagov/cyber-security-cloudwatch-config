""" Generic component helper functions """
import datetime

import boto3
from addict import Dict

from logger import LOG


class GenericHelper:
    """ Standard helper functions for cloudwatch metrics """

    @classmethod
    def get_caller_identity(cls):
        """ Get a session for the IAM role to invoke the health lambda """
        session = boto3.session.Session()
        region = session.region_name
        aws_sts = boto3.client("sts", region_name=region)
        caller = aws_sts.get_caller_identity()
        return Dict(caller)

    @classmethod
    def get_namespace_service(cls, namespace):
        """
        Convert CloudWatch namespace to AWS service name
        """
        clients = {
            "AWS/SQS": "sqs",
            "AWS/Lambda": "lambda",
            "AWS/Firehose": "firehose",
            "AWS/Kinesis": "kinesis",
        }
        client_name = clients.get(namespace, None)

        return client_name

    @classmethod
    def get_client_from_namespace(cls, namespace, region):
        """Convert cloudwatch metric namespace to a boto3 client"""

        # Ensure region is set to current session region if
        # not provided
        if region is None:
            session = boto3.session.Session()
            region = session.region_name

        client_name = cls.get_namespace_service(namespace)
        if client_name:
            client = boto3.client(client_name, region_name=region)
        else:
            client = None
        return client

    @classmethod
    def get_metric_dimension_value(cls, metric, dimension_name):
        """Iterate metric dimensions for value of named dimension"""
        dimension_value = None
        for dim in metric.Dimensions:
            if dim.Name == dimension_name:
                dimension_value = dim.Value
            if dim.name == dimension_name:
                dimension_value = dim.value

        return dimension_value

    @classmethod
    def get_dimension_value_matching_substring(cls, dimensions, match_string):
        """Get Value for Name matching match_string"""
        dim_val = None
        for dim in dimensions:
            if match_string in dim["Name"]:
                dim_val = dim["Value"]
            if match_string in dim["name"]:
                dim_val = dim["value"]

        return dim_val

    @classmethod
    def get_metric_region(cls, metric):
        """
        Use metric.Region if set or default to session region

        When generating alarm config we iterate across multiple
        regions so need to set the region which matches the given
        metric.

        When collecting data the forwarder lambdas run in the
        region where the metric/alarm config lives.
        """
        region = metric.get("Region")
        if region:
            LOG.debug(f"Metric region: {region}")
        else:
            session = boto3.session.Session()
            region = session.region_name
            LOG.debug(f"Using session region: {region}")
        return region

    @classmethod
    def get_metric_resource_name(cls, metric):
        """Query dimensions for field matching *Name*"""
        return cls.get_dimension_value_matching_substring(metric.Dimensions, "Name")

    @classmethod
    def get_metric_resource_id(cls, metric):
        """Query dimensions for field matching *Id*"""
        return cls.get_dimension_value_matching_substring(metric.Dimensions, "Id")

    @classmethod
    def get_metric_statistics(cls, metric, statistic):
        """
        Use get-metric-statistics to calculate appropriate alarm thresholds
        based on typical values eg maximum + 10%

        The period is calculated to match the elapsed time
        """
        # aws cloudwatch get-metric-statistics
        # --start-time="2019-10-20T00:00:00Z" --end-time="2019-10-23T00:00:00Z"
        # --statistics=Maximum --namespace="AWS/SQS" /
        #    --metric-name="ApproximateAgeOfOldestMessage"
        # --period=300 --unit=Seconds --dimensions=Name=QueueName,/
        # Value=csw-prod-audit-account-queue
        # --region=eu-west-1

        region = cls.get_metric_region(metric)

        client = boto3.client("cloudwatch", region)

        x_days = 28
        now = datetime.datetime.now()
        days_ago = now - datetime.timedelta(days=x_days)
        # This should return a single datapoint for the entire period
        # Setting the period to the exact time lapse sometimes returns
        # multiple data points.
        #
        # Aggregating across multiple datapoints is possible but needs
        # to be sensitive to the stat type so an aggregate of maximums
        # would need to take the max and an aggregate of minimums would
        # need to take the min etc.
        #
        # For older data (> 15 days ago)
        # the period must be a multiple of 300 (5 mins)
        #
        # This calculates the total time lapse (in seconds) and adds
        # 5 minutes to ensure only one data point can be returned
        period = (60 * 60 * 24 * x_days) + 300
        stats_response = client.get_metric_statistics(
            Namespace=metric.Namespace,
            MetricName=metric.MetricName,
            Dimensions=metric.Dimensions,
            StartTime=days_ago,
            EndTime=now,
            Period=period,
            Statistics=[statistic],
        )
        return Dict(stats_response)

    @classmethod
    def get_metric_threshold(cls, metric, rule):
        """
        Get single value of statistic and
        """
        statistic_value = 0
        metric_stats = cls.get_metric_statistics(metric, rule.Statistic)
        print(str(metric_stats))

        for datapoint in metric_stats.Datapoints:
            statistic_value = datapoint[rule.Statistic]

        threshold = statistic_value * rule.Multiplier
        LOG.info(
            "Baseline threshold: %s * %s = %s",
            statistic_value,
            rule.Multiplier,
            threshold,
        )
        # The min/max overrides do not have to be set
        # If they are set they override the calculated
        # threshold value
        if "Minimum" in rule and threshold < rule.Minimum:
            LOG.info(
                "Baseline threshold (%s) is less than rule min (%s)",
                threshold,
                rule.Minimum,
            )
            threshold = rule.Minimum
        elif "Maximum" in rule and threshold > rule.Maximum:
            LOG.info(
                "Baseline threshold (%s) is greater than rule max (%s)",
                threshold,
                rule.Minimum,
            )
            threshold = rule.Maximum

        return threshold

    @classmethod
    def tag_list_to_dict(cls, tag_list):
        """ Convert list of Key,Value dicts to dict of Key:Value"""
        tags = {tag["Key"]: tag["Value"] for tag in tag_list}
        return tags

    @classmethod
    def get_tags_for_metric_resource(cls, metric, region=None):
        """ Default method return empty dict if no namespace handler """
        return {}
