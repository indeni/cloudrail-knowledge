from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import dataclasses
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class WorkloadMetadataConfigMode(str, Enum):
    MODE_UNSPECIFIED = None
    GCE_METADATA = 'GCE_METADATA'
    GKE_METADATA = 'GKE_METADATA'

@dataclass
class GcpContainerClusterWorkloadMetadataConfig:
    """
        Attributes:
            mode: (Required) How to expose the node metadata to the workload running on the node.
    """
    mode: WorkloadMetadataConfigMode


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
class GcpContainerClusterNetworkConfig:
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
            metadata: (Optional) A metadata Key/Value pairs assigned to an instance in the cluster.
            shielded_instance_config: (Optional) Shielded Instance configurations.
            workload_metadata_config: (Optional) Metadata configuration to expose to workloads on the node pool.
    """

    def __init__(self,
                 name: str,
                 location: str,
                 cluster_ipv4_cidr: str,
                 enable_shielded_nodes: bool,
                 master_authorized_networks_config: Optional[GcpContainerMasterAuthNetConfig],
                 authenticator_groups_config: Optional[GcpContainerClusterAuthGrpConfig],
                 network_config: GcpContainerClusterNetworkConfig,
                 private_cluster_config: Optional[GcpContainerClusterPrivateClusterConfig],
                 metadata: Optional[dict],
                 shielded_instance_config: GcpContainerClusterShielededInstanceConfig,
                 workload_metadata_config: GcpContainerClusterWorkloadMetadataConfig):

        super().__init__(GcpResourceType.GOOGLE_CONTAINER_CLUSTER)
        self.name: str = name
        self.location: str = location
        self.cluster_ipv4_cidr: str = cluster_ipv4_cidr
        self.enable_shielded_nodes: bool = enable_shielded_nodes
        self.master_authorized_networks_config: Optional[GcpContainerMasterAuthNetConfig] = master_authorized_networks_config
        self.authenticator_groups_config: Optional[GcpContainerClusterAuthGrpConfig] = authenticator_groups_config
        self.network_config: GcpContainerClusterNetworkConfig = network_config
        self.private_cluster_config: Optional[GcpContainerClusterPrivateClusterConfig] = private_cluster_config
        self.metadata: Optional[dict] = metadata
        self.shielded_instance_config: GcpContainerClusterShielededInstanceConfig = shielded_instance_config
        self.workload_metadata_config: GcpContainerClusterWorkloadMetadataConfig = workload_metadata_config

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
                'network_config': self.network_config and dataclasses.asdict(self.network_config),
                'private_cluster_config': self.private_cluster_config and dataclasses.asdict(self.private_cluster_config),
                'metadata': self.metadata,
                'shielded_instance_config': self.shielded_instance_config and dataclasses.asdict(self.shielded_instance_config),
                'workload_metadata_config': self.workload_metadata_config and dataclasses.asdict(self.workload_metadata_config)}

    @property
    def network_policy_enabled(self) -> bool:
        return self.network_config and self.network_config.enabled

    def check_metadata(self, metadata_key: str, metadata_value: str) -> bool:
        return self.metadata and self.metadata.get(metadata_key) == metadata_value
