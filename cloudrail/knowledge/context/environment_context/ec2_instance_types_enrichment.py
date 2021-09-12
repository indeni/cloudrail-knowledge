import functools
import logging

import boto3
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_ec2_instance_type


class Ec2sInstanceTypesEnrichment:

    @staticmethod
    def get_boto_client():
        return boto3.client('ec2')

    def __init__(self, context: AwsEnvironmentContext, client=None):
        self.context = context
        self.client = client or self.get_boto_client()

    def run(self):
        if len(self.context.ec2_instance_types) == 0:
            try:
                instance_types_data = self._collect_instance_types()
                for attributes in instance_types_data['InstanceTypes']:
                    self.context.ec2_instance_types.append(build_ec2_instance_type(attributes))
            except Exception:
                logging.exception('Error while enriching ec2 instance types')
            finally:
                self._collect_instance_types.cache_clear()

    @functools.lru_cache(maxsize=None)
    def _collect_instance_types(self) -> dict:
        return self.client.describe_instance_types()
