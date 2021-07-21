""" SQS component helper functions """
import json

import botocore
from addict import Dict

from components.generic_helper import GenericHelper


class CodePipelineHelper(GenericHelper):
    """ Helper functions for CodePipeline """

    @classmethod
    def get_tags_for_metric_resource(cls, metric):
        """
        Get the Codepipeline tags using the pipeline ARN.
        """
        region = cls.get_metric_region(metric)
        namespace = metric.Namespace
        tags = {}
        try:
            print(f"Getting boto client for {namespace} in {region}")
            client = cls.get_client_from_namespace(namespace, region)
            if client:
                print(f"Get tags for code pipeline: {namespace}")
                codepipeline_arn = metric.resources[0]
                get_tags_response = Dict(client.list_tags_for_resource(resourceArn=codepipeline_arn))
                tags = get_tags_response.tags

        except AttributeError as err:
            print(json.dumps(metric, indent=2))
            print(str(err))
        except botocore.exceptions.ClientError as err:
            print(str(err))
        return tags

