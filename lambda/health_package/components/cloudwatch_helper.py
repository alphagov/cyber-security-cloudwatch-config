""" Cloudwatch component helper functions """
import json

import botocore
from addict import Dict

from ..components.generic_helper import GenericHelper
from ..logger import LOG


class CloudwatchHelper(GenericHelper):
    """ Helper functions for Cloudwatch """

    @classmethod
    def metric_resource_exists(cls, metric, region=None):
        """
        Check the resource exists before defining an alarm
        aws cloudwatch list-metrics returns metrics for resources that
        no longer exists
        """
        namespace = metric.Namespace
        resource_exists = True
        try:
            print(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                event_rule_name = cls.get_metric_dimension_value(metric, "RuleName")
                if event_rule_name:
                    print(f"Get tags for event rule names: {event_rule_name}")
                    client.list_targets_by_rule(Rule=event_rule_name)
                else:
                    resource_exists = False

        except AttributeError as err:
            print(json.dumps(metric, indent=2))
            print(str(err))
        except botocore.exceptions.ClientError as err:
            print(str(err))
            resource_exists = False
        return resource_exists

    @classmethod
    def get_tags_for_metric_resource(cls, metric, region=None):
        namespace = metric.Namespace
        tags = {}
        try:
            print(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                event_rule_name = cls.get_metric_dimension_value(metric, "RuleName")
                if event_rule_name:
                    print(f"Get tags for event rule name: {event_rule_name}")
                    get_function_response = Dict(
                        client.list_targets_by_rule(Rule=event_rule_name)
                        )
                    event_rule_name_arn = get_function_response.Targets.arn
                    get_tags_response = Dict(client.list_tags(Resource=event_rule_name_arn))
                    tags = get_tags_response.Tags

        except AttributeError as err:
            print(json.dumps(metric, indent=2))
            print(str(err))
        except botocore.exceptions.ClientError as err:
            print(str(err))
        return tags

    # @classmethod
    # def get_metric_threshold(cls, metric, rule, region=None):
    #     threshold = super().get_metric_threshold(metric, rule)
    #     # Calculate duration threshold here.
    #
    #     # Get the lambda timeout
    #     namespace = metric.Namespace
    #     # Assign a timeout outside of the try block
    #     lambda_timeout = 60
    #     try:
    #         print(f"Getting boto client for {namespace} in {region}")
    #         client = cls.get_client_from_namespace(namespace, region)
    #         if client:
    #             log_group_name = cls.get_metric_dimension_value(metric, "LogGroupName")
    #             if log_group_name:
    #                 print(f"Get timeout for function: {log_group_name}")
    #                 get_function_response = Dict(
    #                     client.get_function(LogGroupName=log_group_name)
    #                 )
    #                 lambda_timeout = get_function_response.Configuration.Timeout
    #     except AttributeError as err:
    #         print(json.dumps(metric, indent=2))
    #         print(str(err))
    #     except botocore.exceptions.ClientError as err:
    #         print(str(err))
    #
    #     rule.Maximum = lambda_timeout * 0.9
    #
    #     if threshold > rule.Maximum:
    #         LOG.info(
    #             "Baseline threshold (%s) is greater than rule max (%s)",
    #             threshold,
    #             rule.Minimum,
    #         )
    #         threshold = rule.Maximum
    #     return threshold
