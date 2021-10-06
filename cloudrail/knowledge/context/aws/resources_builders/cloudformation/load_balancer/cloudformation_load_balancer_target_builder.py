from typing import Dict, List

from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target import LoadBalancerTarget

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLoadBalancerTargetBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_LOAD_BALANCER_TARGET_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[LoadBalancerTarget]:
        properties: dict = cfn_res_attr['Properties']
        targets: LoadBalancerTarget = [LoadBalancerTarget(target_group_arn=self.get_resource_id(cfn_res_attr),
                                                          target_id=target['Id'],
                                                          port=target['Port'],
                                                          region=cfn_res_attr['region'],
                                                          account=cfn_res_attr['account_id'])
                                       for target in properties.get('Targets', [])]
        return targets
