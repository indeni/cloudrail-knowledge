from typing import Dict

from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group_association import LoadBalancerTargetGroupAssociation

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLoadBalancerTargetGroupAssociationBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_LOAD_BALANCER_LISTENER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> LoadBalancerTargetGroupAssociation:
        properties: dict = cfn_res_attr['Properties']

        target_group_arns = []
        for action in properties['DefaultActions']:
            if 'TargetGroupArn' in action:
                target_group_arns.append(action['TargetGroupArn'])

        return LoadBalancerTargetGroupAssociation(
            target_group_arns=target_group_arns,
            load_balancer_arn=self.get_property(properties, 'LoadBalancerArn'),
            port=self.get_property(properties, 'Port'),
            account=cfn_res_attr['account_id'],
            region=cfn_res_attr['region'])
