""" Cloudwatch component helper functions """
import json

import botocore
from addict import Dict

from components.generic_helper import GenericHelper
from logger import LOG

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
            LOG.info(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                event_rule_name = cls.get_metric_dimension_value(metric, "RuleName")
                if event_rule_name:
                    LOG.info(f"Get tags for event rule names: {event_rule_name}")
                    client.list_targets_by_rule(Rule=event_rule_name)
                else:
                    resource_exists = False

        except AttributeError as err:
            LOG.error(json.dumps(metric, indent=2))
            LOG.error(str(err))
        except botocore.exceptions.ClientError as err:
            LOG.error(str(err))
            resource_exists = False
        return resource_exists

    @classmethod
    def get_tags_for_metric_resource(cls, metric, region=None):
        namespace = metric.Namespace
        tags = {}
        try:
            LOG.info(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                event_rule_name = cls.get_metric_dimension_value(metric, "RuleName")
                if event_rule_name:
                    LOG.info(f"Get tags for event rule name: {event_rule_name}")
                    get_function_response = Dict(
                        client.list_targets_by_rule(Rule=event_rule_name)
                    )
                    event_rule_name_arn = get_function_response.Targets.arn
                    get_tags_response = Dict(
                        client.list_tags(Resource=event_rule_name_arn)
                    )
                    tags = get_tags_response.Tags

        except AttributeError as err:
            LOG.error(json.dumps(metric, indent=2))
            LOG.error(str(err))
        except botocore.exceptions.ClientError as err:
            LOG.error(str(err))
        return tags
