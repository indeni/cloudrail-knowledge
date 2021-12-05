from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_proxy import GcpComputeTargetProxy, TargetTypes
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType


class GcpComputeTargetHttpProxy(GcpComputeTargetProxy):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            target_id: an identifier for the resource with format projects/{{project}}/global/targetHttpProxies/{{name}}
            self_link: (Optional) The URI of the created resource.
            url_map: A reference to the UrlMap resource that defines the mapping from URL to the BackendService.
    """

    def __init__(self,
                 name: str,
                 target_id: str,
                 self_link: str,
                 url_map: str):
        super().__init__(name, self_link, TargetTypes.HTTP, GcpResourceType.GOOGLE_COMPUTE_TARGET_HTTP_PROXY)
        self.target_id: str = target_id
        self.url_map: str = url_map
        self.with_aliases(target_id, self_link)

    def get_keys(self) -> List[str]:
        return [self.self_link]

    def get_id(self) -> str:
        return self.target_id

    @property
    def is_encrypted(self) -> bool:
        return False

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-services/loadbalancing/advanced/targetHttpProxies/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        return 'Compute Target Http Proxy Details'

    def to_drift_detection_object(self) -> dict:
        return {'url_map': self.url_map}
