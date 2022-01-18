from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import dataclasses
from cloudrail.knowledge.context.gcp.resources.binary_authorization.gcp_binary_authorization_policy import GcpBinaryAuthorizationAdmissionRule
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpContainerClusterNetworkingMode(str, Enum):
    VPC_NATIVE = 'VPC_NATIVE'
    ROUTES = 'ROUTES'


class GcpContainerClusterReleaseChannel(str, Enum):
    UNSPECIFIED = None
    RAPID = 'RAPID'
    REGULAR = 'REGULAR'
    STABLE = 'STABLE'


class GcpContainerClusterWorkloadMetadataConfigMode(str, Enum):
    MODE_UNSPECIFIED = None
    GCE_METADATA = 'GCE_METADATA'
    GKE_METADATA = 'GKE_METADATA'


@dataclass
class GcpContainerClusterShielededInstanceConfig:
    """
        Attributes:
            enable_secure_boot: (Optional) Indication whether the instance has Secure Boot enabled.
            enable_integrity_monitoring: (Optional) Indication whether the instance has integrity monitoring enabled.
    """
    enable_secure_boot: bool
    enable_integrity_monitoring: bool


@dataclass
class GcpContainerClusterNodeConfig:
    """
        Attributes:
            metadata: (Optional) A metadata Key/Value pairs assigned to an instance in the cluster.
            shielded_instance_config: (Optional) Shielded Instance configurations.
            workload_metadata_config_mode: (Optional) How to expose the node metadata to the workload running on the node.
            service_account: (Optional) The service account to be used by the Node VMs.
    """
    metadata: dict
    shielded_instance_config: GcpContainerClusterShielededInstanceConfig
    workload_metadata_config_mode: GcpContainerClusterWorkloadMetadataConfigMode
    service_account: str


@dataclass
class GcpContainerClusterPrivateClusterConfig:
    """
        Attributes:
            enable_private_nodes: (Optional) Indication whether nodes have internal IP addresses only.
            enable_private_endpoint: (Optional) Indication whether the master's internal IP address is used as the cluster endpoint.
            master_global_access_config: (Optional) Indication whether the master is accessible globally or not.
    """
    enable_private_nodes: bool
    enable_private_endpoint: bool
    master_global_access_config: bool

class GcpContainerClusterNetworkConfigProvider(str, Enum):
    PROVIDER_UNSPECIFIED = None
    CALICO = 'Tigera'

@dataclass
class GcpContainerClusterNetworkPolicy:
    """
        Attributes:
            provider: (Optional) The selected network policy provider.
            enabled: Whether network policy is enabled on the cluster nodes.
    """
    provider: GcpContainerClusterNetworkConfigProvider
    enabled: bool

@dataclass
class GcpContainerClusterAuthGrpConfig:
    """
        Attributes:
            security_group:(Optional) The name of the RBAC security group for use with Google security groups in Kubernetes RBAC.
    """
    security_group: str


@dataclass
class GcpContainerMasterAuthNetConfigCidrBlk:
    """
        Attributes:
            cidr_block: (Optional) External network that can access Kubernetes master through HTTPS. Must be specified in CIDR notation.
            display_name: (Optional) Field for users to identify CIDR blocks.
    """
    cidr_block: str
    display_name: str


@dataclass
class GcpContainerMasterAuthNetConfig:
    """
        Attributes:
            cidr_blocks: (Optional) External networks that can access the Kubernetes cluster master through HTTPS.
    """
    cidr_blocks: List[GcpContainerMasterAuthNetConfigCidrBlk]


class GcpContainerCluster(GcpResource):
    """
        Attributes:
            name: The name of the cluster, unique within the project and location.
            location: (Optional) The location (region or zone) in which the cluster master will be created, as well as the default node location.
            cluster_ipv4_cidr: (Optional) The IP address range of the Kubernetes pods in this cluster in CIDR notation.
            enable_shielded_nodes: (Optional) Enable Shielded Nodes features on all nodes in this cluster. Defaults to false.
            master_authorized_networks_config: (Optional) The desired configuration options for master authorized networks.
            authenticator_groups_config: (Optional) Configuration for the Google Groups for GKE feature.
            private_cluster_config: (Optional) Configuration for cluster with private nodes.
            release_channel: (Optional) Configuration options for the Release channel feature, which provide more control over automatic upgrades of your GKE clusters.
            issue_client_certificate: (Optional) Whether client certificate authorization is enabled for this cluster.
            pod_security_policy_enabled: (Optional) Whether pods must be valid under a PodSecurityPolicy in ortder to be created.
            network_policy: (Optional) Configuration for the Network Policy of the GKE.
            networking_mode: (Optional) Whether alias IPs or routes will be used for pod IPs in the cluster.
    """

    def __init__(self,
                 name: str,
                 location: str,
                 cluster_ipv4_cidr: str,
                 enable_shielded_nodes: bool,
                 master_authorized_networks_config: Optional[GcpContainerMasterAuthNetConfig],
                 authenticator_groups_config: Optional[GcpContainerClusterAuthGrpConfig],
                 network_policy: GcpContainerClusterNetworkPolicy,
                 private_cluster_config: Optional[GcpContainerClusterPrivateClusterConfig],
                 node_config: GcpContainerClusterNodeConfig,
                 release_channel: GcpContainerClusterReleaseChannel,
                 issue_client_certificate: bool,
                 pod_security_policy_enabled: bool,
                 enable_binary_authorization: bool,
                 networking_mode: GcpContainerClusterNetworkingMode):

        super().__init__(GcpResourceType.GOOGLE_CONTAINER_CLUSTER)
        self.name: str = name
        self.location: str = location
        self.cluster_ipv4_cidr: str = cluster_ipv4_cidr
        self.enable_shielded_nodes: bool = enable_shielded_nodes
        self.master_authorized_networks_config: Optional[GcpContainerMasterAuthNetConfig] = master_authorized_networks_config
        self.authenticator_groups_config: Optional[GcpContainerClusterAuthGrpConfig] = authenticator_groups_config
        self.network_policy: GcpContainerClusterNetworkPolicy = network_policy
        self.private_cluster_config: Optional[GcpContainerClusterPrivateClusterConfig] = private_cluster_config
        self.node_config: GcpContainerClusterNodeConfig = node_config
        self.release_channel: GcpContainerClusterReleaseChannel = release_channel
        self.issue_client_certificate: bool = issue_client_certificate
        self.pod_security_policy_enabled: bool = pod_security_policy_enabled
        self.enable_binary_authorization: bool = enable_binary_authorization
        self.networking_mode: GcpContainerClusterNetworkingMode = networking_mode
        self.binary_auth_policies: List[GcpBinaryAuthorizationAdmissionRule] = []

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return True

    def get_name(self) -> Optional[str]:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/kubernetes/clusters/details/{self.location}/{self.name}/details?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Container Cluster'
        else:
            return 'Container Clusters'

    def to_drift_detection_object(self) -> dict:
        return {'enable_shielded_nodes': self.enable_shielded_nodes,
                'master_authorized_networks_config':self.master_authorized_networks_config and dataclasses.asdict(self.master_authorized_networks_config),
                'authenticator_groups_config':self.authenticator_groups_config and dataclasses.asdict(self.authenticator_groups_config),
                'labels': self.labels,
                'network_policy': self.network_policy and dataclasses.asdict(self.network_policy),
                'private_cluster_config': self.private_cluster_config and dataclasses.asdict(self.private_cluster_config),
                'node_config': self.node_config and dataclasses.asdict(self.node_config),
                'release_channel': self.release_channel,
                'networking_mode': self.networking_mode}

    @property
    def network_policy_enabled(self) -> bool:
        return self.network_policy and self.network_policy.enabled

    def check_node_metadata(self, metadata_key: str, metadata_value: str) -> bool:
        return self.node_config.metadata and self.node_config.metadata.get(metadata_key) == metadata_value
