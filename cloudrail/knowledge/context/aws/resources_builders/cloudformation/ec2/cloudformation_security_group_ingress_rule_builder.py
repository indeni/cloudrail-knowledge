from typing import Dict

from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_security_group_rule_base_builder import CloudformationSecurityGroupRuleBaseBuilder


class CloudformationSecurityGroupIngressRuleBuilder(CloudformationSecurityGroupRuleBaseBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]):
        super().__init__(CloudformationResourceType.SECURITY_GROUP_INGRESS, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> SecurityGroupRule:
        properties: dict = cfn_res_attr['Properties']
        return self.parse_security_group_rule(security_group_rule_properties=cfn_res_attr,
                                              egress=False,
                                              security_group_id=self.get_property(properties, 'GroupId'),
                                              account_id=cfn_res_attr['account_id'],
                                              region=cfn_res_attr['region'])
