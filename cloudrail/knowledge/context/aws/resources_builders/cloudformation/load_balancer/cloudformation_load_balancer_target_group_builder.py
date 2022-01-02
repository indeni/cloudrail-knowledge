from typing import Dict

from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group import LoadBalancerTargetGroup

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLoadBalancerTargetGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_LOAD_BALANCER_TARGET_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> LoadBalancerTargetGroup:
        properties: dict = cfn_res_attr['Properties']
        return LoadBalancerTargetGroup(port=self.get_property(properties, 'Port'),
                                       protocol=self.get_property(properties, 'Protocol'),
                                       vpc_id=self.get_property(properties, 'VpcId'),
                                       target_group_arn=self.get_resource_id(cfn_res_attr),
                                       target_group_name=self.get_name_tag(properties),
                                       target_type=self.get_property(properties, 'TargetType') or 'instance',
                                       region=cfn_res_attr['region'],
                                       account=cfn_res_attr['account_id'])
