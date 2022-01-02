from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_ssl_policy import GcpComputeSslPolicy
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_proxy import GcpComputeTargetProxy, TargetTypes
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType


class GcpComputeTargetSslProxy(GcpComputeTargetProxy):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            target_id: an identifier for the resource with format projects/{{project}}/global/targetSslProxies/{{name}}
            self_link: (Optional) The URI of the created resource.
            backend_service: A reference to the BackendService resource.
            ssl_certificates: A list of SslCertificate resources that are used to authenticate connections between users and the load balancer. At least one SSL certificate must be specified.
            ssl_policy_identifier: (Optional) A reference to the SslPolicy resource that will be associated with the TargetSslProxy resource.
    """

    def __init__(self,
                 name: str,
                 target_id: str,
                 self_link: str,
                 backend_service: str,
                 ssl_certificates: List[str],
                 ssl_policy_identifier: Optional[str]):
        super().__init__(name, self_link, TargetTypes.SSL, GcpResourceType.GOOGLE_COMPUTE_TARGET_SSL_PROXY)
        self.target_id: str = target_id
        self.backend_service: str = backend_service
        self.ssl_certificates: List[str] = ssl_certificates
        self.ssl_policy_identifier: Optional[str] = ssl_policy_identifier
        self.ssl_policy: Optional[GcpComputeSslPolicy] = None
        self.with_aliases(target_id, self_link)

    def get_keys(self) -> List[str]:
        return [self.self_link]

    def get_id(self) -> str:
        return self.target_id

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-services/loadbalancing/advanced/targetHttpProxies/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        return 'Compute Target Ssl Proxy Details'

    @property
    def is_encrypted(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {"ssl_certificates": self.ssl_certificates,
                "backend_service": self.backend_service}
