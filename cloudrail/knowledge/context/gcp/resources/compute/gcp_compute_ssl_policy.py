from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeSslPolicy(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            min_tls_version: (Optional) The minimum version of SSL protocol that can be used by the clients to establish a connection with the load balancer.
                                        Default value is TLS_1_0
            profile: (Optional) Profile specifies the set of SSL features that can be used by the load balancer when negotiating SSL with clients
            custom_features: (Optional) the set of SSL features. if CUSTOM profile is used this attribute must be set.
    """

    def __init__(self,
                 name: str,
                 min_tls_version: Optional[str],
                 profile: Optional[str],
                 custom_features: Optional[List[str]]):

        super().__init__(GcpResourceType.GOOGLE_COMPUTE_SSL_POLICY)
        self.name: str = name
        self.min_tls_version: Optional[str] = min_tls_version
        self.profile: Optional[str] = profile
        self.custom_features: Optional[List[str]] = custom_features

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False

    def get_name(self) -> Optional[str]:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-security/sslpolicies/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        return 'Compute SSL Policy Details'

    def to_drift_detection_object(self) -> dict:
        return {"min_tls_version": self.min_tls_version,
                "profile": self.profile,
                "custom_features": self.custom_features}
