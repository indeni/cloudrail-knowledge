from typing import List, Optional, Dict
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeTargetHttpsProxy(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            ssl_certificates: A list of SslCertificate resources that are used to authenticate connections between users and the load balancer. At least one SSL certificate must be specified.
            url_map: A reference to the UrlMap resource that defines the mapping from URL to the BackendService.
            ssl_policy: (Optional) A reference to the SslPolicy resource that will be associated with the TargetSslProxy resource.
    """

    def __init__(self,
                 name: str,
                 url_map: str,
                 ssl_certificates: List[str],
                 ssl_policy: Optional[str]):

        super().__init__(GcpResourceType.GOOGLE_COMPUTE_TARGET_HTTPS_PROXY)
        self.name: str = name
        self.url_map: str = url_map
        self.ssl_certificates: List[str] = ssl_certificates
        self.ssl_policy: Optional[str] = ssl_policy

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-services/loadbalancing/advanced/targetHttpsProxies/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Compute Target Https Proxy Details'
        else:
            return 'Compute Target Https Proxy Details'

    def to_drift_detection_object(self) -> dict:
        return {'url_map': self.url_map,
                'ssl_certificates': self.ssl_certificates,
                'ssl_policy': self.ssl_policy}
