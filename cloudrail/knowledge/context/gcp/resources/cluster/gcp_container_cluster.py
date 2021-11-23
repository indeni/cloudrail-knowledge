from typing import List, Optional
from dataclasses import dataclass
import dataclasses
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


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
    """

    def __init__(self,
                 name: str,
                 location: str,
                 cluster_ipv4_cidr: str,
                 enable_shielded_nodes: bool,
                 master_authorized_networks_config: Optional[GcpContainerMasterAuthNetConfig],
                 authenticator_groups_config: Optional[GcpContainerClusterAuthGrpConfig]):

        super().__init__(GcpResourceType.GOOGLE_CONTAINER_CLUSTER)
        self.name: str = name
        self.location: str = location
        self.cluster_ipv4_cidr: str = cluster_ipv4_cidr
        self.enable_shielded_nodes: bool = enable_shielded_nodes
        self.master_authorized_networks_config: Optional[GcpContainerMasterAuthNetConfig] = master_authorized_networks_config
        self.authenticator_groups_config: Optional[GcpContainerClusterAuthGrpConfig] = authenticator_groups_config

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
                'labels': self.labels}
