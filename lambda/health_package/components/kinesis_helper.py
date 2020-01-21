""" SQS component helper functions """
import json

import botocore
from addict import Dict

from components.generic_helper import GenericHelper


class KinesisHelper(GenericHelper):
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
            print(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                stream_name = cls.get_metric_dimension_value(metric, "StreamName")
                if stream_name:
                    client.describe_stream(
                        StreamName=stream_name
                    )
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
        """
        Get QueueUrl from queue name and then get the tags if present
        There is some duplication of the above function it would be nice to remove
        """
        namespace = metric.Namespace
        tags = {}
        try:
            print(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                stream_name = cls.get_metric_dimension_value(metric, "StreamName")
                if stream_name:
                    print(f"Get tags for kinesis stream: {stream_name}")
                    list_tags_response = Dict(client.list_tags_for_stream(
                        StreamName=stream_name
                    ))
                    tags = list_tags_response.Tags

        except AttributeError as err:
            print(json.dumps(metric, indent=2))
            print(str(err))
        except botocore.exceptions.ClientError as err:
            print(str(err))
        return tags
