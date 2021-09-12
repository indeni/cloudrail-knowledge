from typing import Dict

from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationEc2Builder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.EC2_INSTANCE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Ec2Instance:
        properties: dict = cfn_res_attr['Properties']
        private_ip = self.get_property(properties, 'PrivateIpAddress')
        public_ip = self.get_property(properties, 'PublicIp')
        ipv6_addresses = self.get_property(properties, 'Ipv6Addresses', [])
        network_interfaces = self.get_property(properties, 'NetworkInterfaces', [])
        network_interface_ids = [ni['NetworkInterfaceId'] for ni in network_interfaces]
        security_groups_ids = self.get_property(properties, 'SecurityGroupIds')
        http_tokens = 'optional'
        ebs_optimized = self.get_property(properties, 'EbsOptimized', False)

        return Ec2Instance(account=cfn_res_attr['account_id'],
                           region=cfn_res_attr['region'],
                           instance_id=self.get_resource_id(cfn_res_attr),
                           name=self.get_name_tag(properties),
                           network_interfaces_ids=network_interface_ids,
                           state=None,
                           image_id=self.get_property(properties, 'ImageId'),
                           iam_profile_name=self.get_property(properties, 'IamInstanceProfile'),
                           http_tokens=http_tokens,
                           availability_zone=self.get_property(properties, 'AvailabilityZone'),
                           tags=self.get_tags(properties) or {},
                           instance_type=self.get_property(properties, 'InstanceType'),
                           ebs_optimized=ebs_optimized,
                           monitoring_enabled=self.get_property(properties, 'Monitoring', False)) \
            .with_raw_data(subnet_id=self.get_property(properties, 'SubnetId'),
                           private_ip_address=private_ip,
                           public_ip_address=public_ip,
                           ipv6_addresses=ipv6_addresses,
                           security_groups_ids=security_groups_ids)
