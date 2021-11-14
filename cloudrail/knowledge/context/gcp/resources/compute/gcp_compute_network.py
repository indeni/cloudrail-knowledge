from typing import List, Optional, Dict
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeNetworkRoutingMode(Enum):
    REGIONAL = 'REGIONAL'
    GLOBAL = 'GLOBAL'


class GcpComputeNetwork(GcpResource):
    """
        Attributes:
        name: (Required) A unique name of the resource.
        auto_create_subnetworks: (Optional) When set to true, the network is created in "auto subnet mode" and it will create a subnet for each region automatically across the 10.128.0.0/9 address range.
        routing_mode: (Optional) The network-wide routing mode to use. Possible values are REGIONAL and GLOBAL.
        delete_default_routes_on_create: (Optional) If set to true, default routes (0.0.0.0/0) will be deleted immediately after network creation.
        project: (Optional) The ID of the project in which the resource belongs.
    """

    def __init__(self,
                 name: str,
                 auto_create_subnetworks: Optional[bool],
                 routing_mode: Optional[GcpComputeNetworkRoutingMode],
                 delete_default_routes_on_create: Optional[bool],
                 project: Optional[str]):
        super().__init__(GcpResourceType.GOOGLE_COMPUTE_NETWORK)
        self.name: str = name
        self.auto_create_subnetworks: Optional[bool] = auto_create_subnetworks
        self.routing_mode: Optional[GcpComputeNetworkRoutingMode] = routing_mode
        self.delete_default_routes_on_create: Optional[bool] = delete_default_routes_on_create
        self.project: Optional[str] = project

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/networking/networks/details/{self.name}?project={self.project}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Compute Network Details'
        else:
            return 'Compute Network Details'
