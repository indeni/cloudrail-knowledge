from typing import Dict, List

from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_security_group_rule_base_builder import CloudformationSecurityGroupRuleBaseBuilder


class CloudformationSecurityGroupInlineRuleBuilder(CloudformationSecurityGroupRuleBaseBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]):
        super().__init__(CloudformationResourceType.SECURITY_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[SecurityGroupRule]:
        rules = []
        properties: dict = cfn_res_attr['Properties']

        rules.extend(self.parse_security_group_rule(security_group_rule_properties=ingress_rule_property,
                                                    egress=False,
                                                    security_group_id=self.get_resource_id(cfn_res_attr),
                                                    account_id=cfn_res_attr['account_id'],
                                                    region=cfn_res_attr['region']) for ingress_rule_property in self.get_property(properties, 'SecurityGroupIngress', []))

        rules.extend(self.parse_security_group_rule(security_group_rule_properties=egress_rule_property,
                                                    egress=True,
                                                    security_group_id=self.get_resource_id(cfn_res_attr),
                                                    account_id=cfn_res_attr['account_id'],
                                                    region=cfn_res_attr['region']) for egress_rule_property in self.get_property(properties, 'SecurityGroupEgress', []))

        return rules
