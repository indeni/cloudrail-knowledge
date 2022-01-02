from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource

class DnsDefKeyAlgorithm(str, Enum):
    NONE = 'None'
    ECDSAP256SHA256 = 'ecdsap256sha256'
    ECDSAP384SHA384 = 'ecdsap384sha384'
    RSASHA1 = 'rsasha1'
    RSASHA256 = 'rsasha256'
    RSASHA512 = 'rsasha512'

class DnsDefKeyType(str, Enum):
    NONE = 'None'
    KEYSIGNING = 'keySigning'
    ZONESIGNING = 'zoneSigning'


@dataclass
class GcpDnsManagedZoneDnsSecCfgDefKeySpecs:
    """
        Attributes:
            algorithm: (Optional) String mnemonic specifying the DNSSEC algorithm of this key Possible values are ecdsap256sha256, ecdsap384sha384, rsasha1, rsasha256, and rsasha512.
            key_length: (Optional) Length of the keys in bits.
            key_type: (Optional) (Optional) Specifies whether this is a key signing key (KSK) or a zone signing key (ZSK).
            kind: (Optional) Identifies the kind of resource.
    """
    algorithm: DnsDefKeyAlgorithm
    key_length: int
    key_type: DnsDefKeyType
    kind: str


@dataclass
class GcpDnsManagedZoneDnsSecCfg:
    """
        Attributes:
            kind: (Optional) Identifies the kind of resource.
            non_existence: (Optional) Specifies the mechanism used to provide authenticated denial-of-existence responses. Possible values are nsec and nsec3.
            state: (Optional) Specifies whether DNSSEC is enabled, and what mode it is in. Possible values are off, on, and transfer.
            default_key_specs: (Optional) Specifies parameters that will be used for generating initial DnsKeys for this ManagedZone.
    """
    kind: str
    non_existence: Optional[str]
    state: str
    default_key_specs: List[GcpDnsManagedZoneDnsSecCfgDefKeySpecs]


class GcpDnsManagedZone(GcpResource):
    """
        Attributes:
            name: (Required) User assigned name for this resource. Must be unique within the project.
            dns_name: (Required) The DNS name of this managed zone.
            description: (Optional) A textual description field.
            dnssec_config: (Optional) DNSSEC configuration parameters.
    """

    def __init__(self,
                 name: str,
                 dns_name: str,
                 description: Optional[str],
                 dnssec_config: Optional[GcpDnsManagedZoneDnsSecCfg]):

        super().__init__(GcpResourceType.GOOGLE_DNS_MANAGED_ZONE)
        self.name: str = name
        self.dns_name: str = dns_name
        self.description: Optional[str] = description
        self.dnssec_config: Optional[GcpDnsManagedZoneDnsSecCfg] = dnssec_config

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return True

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-services/dns/zones/{self.name}/?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'DNS Managed Zone'
        else:
            return 'DNS Managed Zones'

    def to_drift_detection_object(self) -> dict:
        return {'labels': self.labels,
                'description': self.description,
                'dnssec_config': self.dnssec_config}
