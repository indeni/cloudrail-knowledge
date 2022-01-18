import dataclasses
from typing import List, Optional
from dataclasses import dataclass

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerClusterNodeConfig
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


@dataclass
class GcpClusterNodePoolAutoscaling:
    """
        Attributes:
            min_node_count: (Required) Minimum number of nodes in the NodePool. Must be >=0 and <= max_node_count.
            max_node_count: (Required) Maximum number of nodes in the NodePool. Must be >= min_node_count.
    """
    min_node_count: int
    max_node_count: int


@dataclass
class GcpClusterNodePoolManagement:
    """
        Attributes:
            auto_repair: (Optional) Whether the nodes will be automatically repaired.
            auto_upgrade: (Optional) Whether the nodes will be automatically upgraded.
    """
    auto_repair: bool
    auto_upgrade: bool


class GcpContainerNodePool(GcpResource):
    """
        Attributes:
            name: (Optional) The name of the node pool.
            cluster: The name of the cluster to create the node pools.
            location: (Optional) The location (region or zone) of the cluster.
            autoscaling: (Optional) Configuration required by cluster autoscaler to adjust the size of the node pool to the current cluster usage.
            management: (Optional) Node management configuration, wherein auto-repair and auto-upgrade is configured.
            node_config: (Optional) (Optional) Parameters used in creating the node pool.
    """

    def __init__(self,
                 name: str,
                 cluster: str,
                 location: Optional[str],
                 autoscaling: Optional[GcpClusterNodePoolAutoscaling],
                 management: GcpClusterNodePoolManagement,
          		 node_config: GcpContainerClusterNodeConfig):

        super().__init__(GcpResourceType.GOOGLE_CONTAINER_NODE_POOL)
        self.name: str = name
        self.cluster: str = cluster
        self.location: Optional[str] = location
        self.autoscaling: Optional[GcpClusterNodePoolAutoscaling] = autoscaling
        self.management: GcpClusterNodePoolManagement = management
        self.node_config: GcpContainerClusterNodeConfig = node_config


    def get_keys(self) -> List[str]:
        return [self.name, self.location, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/kubernetes/nodepool/{self.location}/{self.cluster}/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Container Cluster Node Pool'
        else:
            return 'Container Clusters Node Pools'

    def to_drift_detection_object(self) -> dict:
        return {'cluster': self.cluster,
                'autoscaling': self.autoscaling and dataclasses.asdict(self.autoscaling),
                'management': self.management and dataclasses.asdict(self.management),
                'node_config': self.node_config and dataclasses.asdict(self.node_config)}
