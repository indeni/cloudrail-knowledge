from typing import Dict, List
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc


class CloudformationVpcBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.VPC, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Vpc:
        resource_properties: dict = cfn_res_attr['Properties']
        cidr_blocks: List[str] = [self.get_property(resource_properties, 'CidrBlock')] if self.get_property(resource_properties, 'CidrBlock') else []
        vpc_id = self.get_resource_id(cfn_res_attr)
        return Vpc(vpc_id=vpc_id,
                   cidr_block=cidr_blocks,
                   ipv6_cidr_block=None,  # todo - support ipv6
                   name=self.get_name_tag(resource_properties),
                   account=cfn_res_attr['account_id'],
                   region=cfn_res_attr['region'],
                   enable_dns_hostnames=self.get_property(resource_properties, 'EnableDnsHostnames'),
                   enable_dns_support=self.get_property(resource_properties, 'EnableDnsSupport')) \
            .with_raw_data(main_route_table_id='',
                           default_route_table_id='',
                           default_security_group_id=f'{vpc_id}.DefaultSecurityGroup')
