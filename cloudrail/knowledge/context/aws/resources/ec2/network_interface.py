from typing import List, Optional

from cloudrail.knowledge.context.connection import ConnectionInstance
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class NetworkInterface(ConnectionInstance, AwsResource):
    """
        Represents a network interface that can be assigned to a specific
        network-bound resource. Sometimes NetworkInterfaces may be auto-generated
        by Cloudrail to provide more data in the context.

        Attributes:
            eni_id: The ID of the elastic network interface.
            subnet_id: The ID of the subnet it's attached to.
            subnet: The actual Subnet object if found.
            primary_ip_address: The primary IP address attached to the interface.
            secondary_ip_addresses: List of secondary IP addresses attached to the
                interface, if any exist.
            public_ip_address: The public IP address of the interface, if it has one.
            ipv6_ip_addresses: The IPv6 addresses of the interface, if they are configured.
            security_groups_ids: The security groups attached to the interface
            security_groups: The actual SGs the interface uses.
            description: The description set for the interface, if any.
            is_primary: True if it's the primary interface for the resource it
                is attached to.
            availability_zone: The AZ this interface is in.
            owner: The resource that owns this interface.
    """

    def __init__(self,
                 eni_id: str,
                 subnet_id: str,
                 primary_ip_address: str,
                 secondary_ip_addresses: List[str],
                 public_ip_address: Optional[str],
                 ipv6_ip_addresses: List[str],
                 security_groups_ids: List[str],
                 description: str,
                 is_primary: bool,
                 availability_zone: Optional[str],
                 account: str,
                 region: str):
        AwsResource.__init__(self, account, region, AwsServiceName.AWS_NETWORK_INTERFACE)
        self.eni_id: str = eni_id
        self.subnet_id: str = subnet_id
        self.primary_ip_address: str = primary_ip_address
        self.secondary_ip_addresses: List[str] = secondary_ip_addresses
        self.public_ip_address: Optional[str] = public_ip_address
        self.ipv6_ip_addresses: List[str] = ipv6_ip_addresses
        self.security_groups_ids: List[str] = security_groups_ids
        self.description: str = description
        self.is_primary: bool = is_primary
        self.availability_zone: str = availability_zone
        self.subnet: 'Subnet' = None
        self.security_groups: List['SecurityGroup'] = []
        self.owner: Optional[AwsResource] = None
        self.with_aliases(eni_id)

        ConnectionInstance.__init__(self)

    @property
    def all_ip_addresses(self) -> List[str]:
        ips = self.secondary_ip_addresses + self.ipv6_ip_addresses + [self.primary_ip_address]
        if self.public_ip_address:
            ips.append(self.public_ip_address)

        return list(filter(None, ips))

    @property
    def private_ip_addresses(self) -> List[str]:
        return list(filter(None, self.secondary_ip_addresses + [self.primary_ip_address]))

    @property
    def vpc_id(self) -> str:
        return self.subnet.vpc_id

    @property
    def vpc(self) -> 'Vpc':
        return self.subnet.vpc

    def get_keys(self) -> List[str]:
        return [self.eni_id]

    def get_id(self) -> str:
        return self.eni_id

    def get_extra_data(self) -> str:
        subnet_id = 'subnet_id: {}'.format(self.subnet_id) if self.subnet_id else ''
        primary_ip_address = 'primary_ip_address: {}'.format(self.primary_ip_address) if self.primary_ip_address else ''
        public_ip_address = 'security_group_ids: {}'.format(self.public_ip_address) if self.public_ip_address else ''
        availability_zone = 'availability_zone: {}'.format(self.availability_zone) if self.availability_zone else ''
        return ', '.join([subnet_id, primary_ip_address, public_ip_address, availability_zone])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ENI'
        else:
            return "ENI's"

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#NetworkInterface:networkInterfaceId={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.eni_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

    def add_security_group(self, security_group: 'SecurityGroup'):
        self.security_groups.append(security_group)
        security_group.add_usage(self)

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'subnet_id': self.subnet_id,
                'security_groups_ids': self.security_groups_ids,
                'description': self.description,
                'is_primary': self.is_primary,
                'availability_zone': self.availability_zone}
