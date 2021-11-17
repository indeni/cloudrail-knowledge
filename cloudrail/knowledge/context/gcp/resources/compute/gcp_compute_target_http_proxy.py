from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeTargetHttpProxy(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            url_map: A reference to the UrlMap resource that defines the mapping from URL to the BackendService.
    """

    def __init__(self,
                 name: str,
                 url_map: str):

        super().__init__(GcpResourceType.GOOGLE_COMPUTE_TARGET_HTTP_PROXY)
        self.name: str = name
        self.url_map: str = url_map

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-services/loadbalancing/advanced/targetHttpProxies/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        return 'Compute Target Http Proxy Details'


    def to_drift_detection_object(self) -> dict:
        return {'url_map': self.url_map}
