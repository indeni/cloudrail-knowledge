from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeTargetPool(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            region: (Optional) Where the target pool resides. Defaults to project region.
            instances: (Optional) (Optional) List of instances in the pool.
            self_link: The URL self link used for this resource.
    """

    def __init__(self,
                 name: str,
                 region: Optional[str],
                 instances: Optional[List[str]],
                 self_link: str):
        super().__init__(GcpResourceType.GOOGLE_COMPUTE_TARGET_POOL)
        self.name: str = name
        self.region: Optional[str] = region
        self.instances: Optional[List[str]] = instances
        self.self_link: str = self_link
        self.with_aliases(self.get_id())


    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    def get_id(self) -> str:
        return self.self_link

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-services/loadbalancing/advanced/targetPools/details/regions/{self.region}/targetPools/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Compute Target Pool'
        else:
            return 'Compute Target Pools'

    def to_drift_detection_object(self) -> dict:
        return {'instances': self.instances}
