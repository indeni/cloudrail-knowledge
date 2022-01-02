from typing import Dict

from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationSecurityGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.SECURITY_GROUP, cfn_by_type_map)

    # See 'Ref' doc: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html
    def parse_resource(self, cfn_res_attr: dict) -> SecurityGroup:
        properties: dict = cfn_res_attr['Properties']
        vpc_id = self.get_property(properties, 'VpcId')
        name = (self.get_property(properties, 'GroupName', self.get_name_tag(properties)
                                  or self.create_random_pseudo_identifier())) \
                                      if vpc_id else self.get_resource_id(cfn_res_attr)
        security_group_id = self.get_resource_id(cfn_res_attr) if vpc_id else name
        security_group: SecurityGroup = SecurityGroup(security_group_id=security_group_id,
                                                      region=cfn_res_attr['region'],
                                                      account=cfn_res_attr['account_id'],
                                                      name=name,
                                                      vpc_id=vpc_id,
                                                      is_default=False,
                                                      has_description=bool(self.get_property(properties, 'GroupDescription')))

        return security_group
