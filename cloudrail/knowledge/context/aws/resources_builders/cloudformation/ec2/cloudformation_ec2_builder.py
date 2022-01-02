from typing import Dict

from cloudrail.knowledge.utils.utils import flat_list, is_iterable_with_values
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance, AssociatePublicIpAddress
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
        network_interface_ids = [ni.get('NetworkInterfaceId') for ni in network_interfaces]
        network_interface_ids = network_interface_ids if is_iterable_with_values(network_interface_ids) else self.CFN_PSEUDO_LIST
        security_group_ids_from_enis = set(flat_list([ni['GroupSet'] for ni in network_interfaces if ni.get('GroupSet')]))
        security_groups_ids_from_resource = [sg_id for sg_id in self.get_property(properties, 'SecurityGroupIds', [])
                                             if sg_id is not None and '.' not in sg_id]
        security_groups_ids_from_resource = security_groups_ids_from_resource if is_iterable_with_values(security_groups_ids_from_resource) else None
        security_groups_ids = security_groups_ids_from_resource \
            or (security_group_ids_from_enis if is_iterable_with_values(security_group_ids_from_enis) else None)
        associate_public_ip_address_data = [ni.get('AssociatePublicIpAddress') for ni in network_interfaces if ni.get('DeviceIndex') == '0']
        associate_public_ip_address = AssociatePublicIpAddress.convert_from_optional_boolean(associate_public_ip_address_data[0]
                                                                                             if is_iterable_with_values(associate_public_ip_address_data)
                                                                                             else None)
        subnet_id_from_resource = self.get_property(properties, 'SubnetId')
        subnet_ids_from_enis = [ni.get('SubnetId') for ni in network_interfaces]
        subnet_id = subnet_id_from_resource or (subnet_ids_from_enis[0] if is_iterable_with_values(subnet_ids_from_enis) else None)
        http_tokens = 'optional'
        ebs_optimized = self.get_property(properties, 'EbsOptimized', False)

        return Ec2Instance(account=cfn_res_attr['account_id'],
                           region=cfn_res_attr['region'],
                           instance_id=self.get_resource_id(cfn_res_attr),
                           name=self.get_name_tag(properties),
                           network_interfaces_ids=network_interface_ids,
                           state='running',
                           image_id=self.get_property(properties, 'ImageId'),
                           iam_profile_name=self.get_property(properties, 'IamInstanceProfile'),
                           http_tokens=http_tokens,
                           availability_zone=self.get_property(properties, 'AvailabilityZone'),
                           tags=self.get_tags(properties) or {},
                           instance_type=self.get_property(properties, 'InstanceType'),
                           ebs_optimized=ebs_optimized,
                           monitoring_enabled=self.get_property(properties, 'Monitoring', False)) \
            .with_raw_data(subnet_id=subnet_id,
                           private_ip_address=private_ip,
                           public_ip_address=public_ip,
                           ipv6_addresses=ipv6_addresses,
                           security_groups_ids=security_groups_ids,
                           associate_public_ip_address=associate_public_ip_address)
