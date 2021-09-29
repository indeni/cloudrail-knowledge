from typing import Dict

from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationSecurityGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.SECURITY_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> SecurityGroup:
        properties: dict = cfn_res_attr['Properties']
        security_group: SecurityGroup = SecurityGroup(security_group_id=self.get_resource_id(cfn_res_attr),
                                                      region=cfn_res_attr['region'],
                                                      account=cfn_res_attr['account_id'],
                                                      name=self.get_property(properties, 'GroupName') or self.get_name_tag(properties),
                                                      vpc_id=self.get_property(properties, 'VpcId'),
                                                      is_default=False,
                                                      has_description=bool(self.get_property(properties, 'GroupDescription')))

        return security_group
