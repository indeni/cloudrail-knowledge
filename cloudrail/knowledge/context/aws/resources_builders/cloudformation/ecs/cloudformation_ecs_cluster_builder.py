from typing import Dict, List

from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_cluster import EcsCluster
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import LaunchType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.load_balancing_configuration import LoadBalancingConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationEcsClusterBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ECS_CLUSTER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> EcsCluster:
        properties: dict = cfn_res_attr['Properties']
        is_container_insights_enabled = True  # TODO: check the default
        if settings := properties.get('ClusterSettings'):
            is_container_insights_enabled = bool(settings[0]['Value'] == 'enabled')

        cluster_id = self.get_resource_id(cfn_res_attr)
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        cluster_name = self.get_property(properties, 'ClusterName', cluster_id)
        cluster_arn = build_arn('ecs', region, account, 'cluster', None, cluster_name)
        cluster: EcsCluster = EcsCluster(account=account,
                                         region=region,
                                         cluster_arn=cluster_arn,
                                         cluster_id=cluster_id,
                                         cluster_name=cluster_name,
                                         is_container_insights_enabled=is_container_insights_enabled)
        return cluster
