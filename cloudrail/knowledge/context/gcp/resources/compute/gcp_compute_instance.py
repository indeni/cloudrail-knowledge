from typing import List, Optional
from enum import Enum
from dataclasses import dataclass, asdict

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


@dataclass
class GcpComputeInstanceServiceAccount:
    """
        Attributes:
            email: (Optional) The service account e-mail address. If not given, the default Google Compute Engine service account is used.
            scopes: A list of service scopes. Both OAuth2 URLs and gcloud short names are supported.
    """
    email: Optional[str]
    scopes: str


@dataclass
class GcpComputeInstanceShieldInstCfg:
    """
        Attributes:
            enable_secure_boot: (Optional) Verify the digital signature of all boot components, and halt the boot process on failure.
            enable_vtpm: (Optional) Use a virtualized trusted platform module, to encrypt objects like keys and certificates.
            enable_integrity_monitoring: (Optional) Compare the most recent boot measurements to the integrity policy baseline and return a pair of pass/fail results.
    """
    enable_secure_boot: Optional[bool] = False
    enable_vtpm: Optional[bool] = True
    enable_integrity_monitoring: Optional[bool] = True


class GcpComputeInstance(GcpResource):
    """
        Attributes:
            name: A unique name for the compute instance.
            zone: The zone this compute instance located at.
            network_interfaces: Networks to attach to the instance.
            can_ip_forward: (Optional) Whether to allow sending and receiving of packets with non-matching source or destination IPs.
            hostname: (Optional) A custom hostname for the instance.
            metadata: (Optional) Metadata key/value pairs to make available from within the instance.
            service_account: (Optional) Service account to attach to the instance.
            shielded_instance_config: (Optional) Enable Shielded VM on this instance.
    """
    def __init__(self,
                 name: str,
                 zone: str,
                 network_interfaces: Optional[List[GcpComputeInstanceNetworkInterface]],
                 can_ip_forward: Optional[bool],
                 hostname: Optional[str],
                 metadata: Optional[List[str]],
                 service_account: Optional[GcpComputeInstanceServiceAccount],
                 shielded_instance_config: Optional[GcpComputeInstanceShieldInstCfg],
                 instance_id: Optional[str]):

        super().__init__(GcpResourceType.GOOGLE_COMPUTE_INSTANCE)
        self.name: str = name
        self.zone: str = zone
        self.network_interfaces: Optional[List[GcpComputeInstanceNetworkInterface]] = network_interfaces
        self.can_ip_forward: bool = can_ip_forward
        self.hostname: str = hostname
        self.metadata: List[str] = metadata
        self.service_account: Optional[GcpComputeInstanceServiceAccount] = service_account
        self.shielded_instance_config: Optional[GcpComputeInstanceShieldInstCfg] = shielded_instance_config
        self.instance_id: Optional[str] = instance_id

    def get_keys(self) -> List[str]:
        return [self.instance_id]

    def get_id(self) -> str:
        return self.instance_id

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/compute/instancesDetail/zones/{self.zone}/instances/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Virtual Machine Instance'
        else:
            return 'Virtual Machine Instances'

    @property
    def is_tagable(self) -> bool:
        return True

    @property
    def is_labeled(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'network_interfaces': self.network_interfaces and
                                      [asdict(dd_obj) for dd_obj in self.network_interfaces],
                'can_ip_forward': self.can_ip_forward,
                'hostname': self.hostname,
                'metadata': self.metadata,
                'service_account': self.service_account and asdict(self.service_account),
                'shielded_instance_config': self.shielded_instance_config and
                                            asdict(self.shielded_instance_config),
                'labels': self.labels}

    @property
    def is_using_default_service_account(self) -> bool:
        return self.service_account and (not self.service_account.email \
            or ('-' in self.service_account.email and self.service_account.email.split('-')[0].isnumeric() \
                and self.service_account.email.split('-')[1] == 'compute@developer.gserviceaccount.com'))
