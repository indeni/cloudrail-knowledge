from typing import Dict

from cloudrail.knowledge.context.aws.resources.batch.batch_compute_environment import BatchComputeEnvironment
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationBatchComputeEnvironmentBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.BATCH_COMPUTE_ENVIRONMENT, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> BatchComputeEnvironment:
        properties: dict = cfn_res_attr['Properties']
        pseudo_name = self.create_random_pseudo_identifier()
        compute_name = self.get_property(properties, 'ComputeEnvironmentName', f'{pseudo_name}')
        compute_settings = properties.get('ComputeResources')
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        vpc_config = None
        if compute_settings:
            security_group_ids = self.get_property(compute_settings, 'SecurityGroupIds')
            subnet_ids = self.get_property(compute_settings, 'Subnets')
            vpc_config = NetworkConfiguration(False, security_group_ids, subnet_ids) if security_group_ids and subnet_ids else None
        return BatchComputeEnvironment(compute_name=compute_name,
                                       arn=f'arn:aws:batch:{region}:{account}:compute-environment/{compute_name}',
                                       account=account,
                                       region=region,
                                       vpc_config=vpc_config)
