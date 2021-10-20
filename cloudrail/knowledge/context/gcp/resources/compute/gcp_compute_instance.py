from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource

class GcpComputeInstanceNetIntfNicType(Enum):
    GVNIC  = 'gvnic'
    VIRTIO_NET = 'virtio_net'

@dataclass
class GcpComputeInstanceNetIntfAliasIpRange:
    """
        Attributes:
            ip_cidr_range: The IP CIDR range represented by this alias IP range.
            subnetwork_range_name: (Optional) The subnetwork secondary range name specifying the secondary range.
    """
    ip_cidr_range: str
    subnetwork_range_name: Optional[str]

@dataclass
class GcpComputeInstanceNetIntfAccessCfg:
    """
        Attributes:
            nat_ip: (Optional) The IP address that will be 1:1 mapped to the instance's network ip.
            public_ptr_domain_name: (Optional) The DNS domain name for the public PTR record.
            network_tier: (Optional) The networking tier used for configuring this instance. Possible values: PREMIUM, STANDARD.
    """
    nat_ip: Optional[str]
    public_ptr_domain_name: Optional[str]
    network_tier: Optional[str] = 'PREMIUM'

@dataclass
class GcpComputeInstanceNetworkInterface:
    """
        Attributes:
            network: (Optional) The name or self_link of the network to attach this interface to.
            subnetwork: (Optional) The name or self_link of the subnetwork to attach this interface to.
            subnetwork_project: (Optional) The project in which the subnetwork belongs.
            network_ip: (Optional) The private IP address to assign to the instance.
            access_config: (Optional) Access configurations, i.e. IPs via which this instance can be accessed via the Internet.
            alias_ip_range: (Optional) An array of alias IP ranges for this network interface.
            nic_type: (Optional) The type of vNIC to be used on this interface. Possible values: GVNIC, VIRTIO_NET.

    """
    network: Optional[str]
    subnetwork: Optional[str]
    subnetwork_project: Optional[str]
    network_ip: Optional[str]
    access_config: Optional[List[GcpComputeInstanceNetIntfAccessCfg]]
    alias_ip_range: Optional[List[GcpComputeInstanceNetIntfAliasIpRange]]
    nic_type: Optional[GcpComputeInstanceNetIntfNicType]


class GcpComputeInstance(GcpResource):
    """
        Attributes:
            name: A unique name for the compute instance.
            network_interfaces: Networks to attach to the instance.
            can_ip_forward: (Optional) Whether to allow sending and receiving of packets with non-matching source or destination IPs.
            hostname: (Optional) A custom hostname for the instance.
            metadata: (Optional) Metadata key/value pairs to make available from within the instance.
            project: (Optional) The ID of the project in which the resource belongs.
            service_account: (Optional) Service account to attach to the instance.
            shielded_instance_config: (Optional) Enable Shielded VM on this instance.
    """
    def __init__(self,
                 name: str,
                 network_interfaces: Optional[List[GcpComputeInstanceNetworkInterface]],
                 can_ip_forward: Optional[bool],
                 hostname: Optional[str],
                 metadata: Optional[List[str]],
                 project: Optional[str],
                 service_account: Optional[GcpComputeInstanceServiceAcount],
                 shielded_instance_config: Optional[GcpComputeInstanceShieldInstCfg]):

        super().__init__(GcpResourceType.GOOGLE_COMPUTE_INSTANCE)
        self.name: str = name
        self.network_interfaces: Optional[List[GcpComputeInstanceNetworkInterface]] = network_interfaces
        self.can_ip_forward: bool = can_ip_forward
        self.hostname: str = hostname
        self.metadata: List[str] = metadata
        self.project: str = project
        self.service_account: Optional[GcpComputeInstanceServiceAcount] = service_account
        self.shielded_instance_config: Optional[GcpComputeInstanceShieldInstCfg] = shielded_instance_config

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/compute/instancesDetail/zones/{self.zone}/instances/{self.name}?project={self.project}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Virtual Machine Instance'
        else:
            return 'Virtual Machine Instances'

    @property
    def is_tagable(self) -> bool:
        return True
