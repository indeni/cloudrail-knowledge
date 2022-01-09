from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.constants.networking import AddressProtocolVersion


class FrontendIpConfigurationAvailabilityZone(str, Enum):
    ZONE_REDUNDANT = 'Zone-Redundant'
    ZONE_1 = '1'
    ZONE_2 = '2'
    ZONE_3 = '3'
    NO_ZONE = 'No-Zone'


class PrivateIpAddressAllocation(str, Enum):
    DYNAMIC = 'dynamic'
    STATIC = 'static'


@dataclass
class LoadBalancerFrontendIpConfiguration:
    """
        Attributes:
            name: The name of the frontend ip configuration.
            availability_zone: A list of Availability Zones which the Load Balancer's IP addresses should be created in.
            subnet_id: The ID of the Subnet which should be associated with the IP configuration.
            gateway_load_balancer_frontend_ip_configuration_id: The frontend IP configuration ID of a Gateway Sku Load Balancer.
            private_ip_address: Private IP address to assign to the Load Balancer.
            private_ip_address_allocation: The allocation method for the Private IP Address.
            private_ip_address_version: The version of IP that the Private Address is.
            public_ip_address_id: The ID of a public IP address which should be associated with the Load Balancer.
            public_ip_prefix_id: The ID of a public IP prefix which should be associated with the Load Balancer.
    """
    name: str
    availability_zone: List[FrontendIpConfigurationAvailabilityZone]
    subnet_id: Optional[str]
    gateway_load_balancer_frontend_ip_configuration_id: Optional[str]
    private_ip_address: Optional[str]
    private_ip_address_allocation: Optional[PrivateIpAddressAllocation]
    private_ip_address_version: Optional[AddressProtocolVersion]
    public_ip_address_id: Optional[str]
    public_ip_prefix_id: Optional[str]

    def to_drift_detection_object(self) -> dict:
        return {
            'name': self.name,
            'availability_zone': [az.value for az in self.availability_zone],
            'subnet_id': self.subnet_id,
            'gateway_load_balancer_frontend_ip_configuration_id': self.gateway_load_balancer_frontend_ip_configuration_id,
            'private_ip_address': self.private_ip_address,
            'private_ip_address_allocation': self.private_ip_address_allocation and self.private_ip_address_allocation.value,
            'private_ip_address_version': self.private_ip_address_version and self.private_ip_address_version.value,
            'public_ip_address_id': self.public_ip_address_id,
            'public_ip_prefix_id': self.public_ip_prefix_id
        }
