from typing import Dict
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationSubnetBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.SUBNET, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Subnet:
        properties: dict = cfn_res_attr['Properties']
        return Subnet(subnet_id=self.get_resource_id(cfn_res_attr),
                      vpc_id=self.get_property(properties, 'VpcId'),
                      cidr_block=self.get_property(properties, 'CidrBlock'),
                      name=self.get_name_tag(properties),
                      availability_zone=self.get_property(properties, 'AvailabilityZone'),
                      map_public_ip_on_launch=bool(self.get_property(properties, 'MapPublicIpOnLaunch')),
                      region=cfn_res_attr['region'],
                      is_default=False,
                      account=cfn_res_attr['account_id'])
