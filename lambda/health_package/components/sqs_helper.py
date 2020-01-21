""" SQS component helper functions """
import json

import botocore
from addict import Dict

from components.generic_helper import GenericHelper
from logger import LOG


class SqsHelper(GenericHelper):
    """ Helper functions for SQS """
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
            LOG.debug("Getting boto client for %s in %s", namespace, region)
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                queue = cls.get_metric_dimension_value(metric, "QueueName")
                LOG.debug("Get tags for sqs queue: %s", queue)
                if queue:
                    client.get_queue_url(QueueName=queue)
                else:
                    resource_exists = False

        except AttributeError as err:
            LOG.debug(json.dumps(metric, indent=2))
            LOG.debug(str(err))
        except botocore.exceptions.ClientError as err:
            LOG.debug(str(err))
            resource_exists = False
        return resource_exists

    @classmethod
    def get_tags_for_metric_resource(cls, metric, region=None):
        """
        Get QueueUrl from queue name and then get the tags if present
        There is some duplication of the above function it would be nice to remove
        """
        namespace = metric.Namespace
        tags = {}
        try:
            LOG.debug("Getting boto client for %s in %s", namespace, region)
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                caller = cls.get_caller_identity()
                queue = cls.get_metric_dimension_value(metric, "QueueName")
                LOG.debug("Get tags for sqs queue: %s", queue)
                # get_queue_url is not granted by security audit role
                queue_url = f"https://{region}.queue.amazonaws.com/{caller.Account}/{queue}"
                get_tags_response = Dict(client.list_queue_tags(QueueUrl=queue_url))
                LOG.debug(json.dumps(get_tags_response.Tags, indent=2))
                tags = get_tags_response.Tags

        except AttributeError as err:
            LOG.debug(json.dumps(metric, indent=2))
            LOG.debug(str(err))
        except botocore.exceptions.ClientError as err:
            LOG.debug(str(err))
        return tags
