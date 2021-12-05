from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeSslPolicy(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            policy_id: an identifier for the resource with format projects/{{project}}/global/sslPolicies/{{name}}
            self_link: (Optional) The URI of the created resource.
            min_tls_version: (Optional) The minimum version of SSL protocol that can be used by the clients to establish a connection with the load balancer.
                                        Default value is TLS_1_0
            profile: (Optional) Profile specifies the set of SSL features that can be used by the load balancer when negotiating SSL with clients
            custom_features: (Optional) the set of SSL features. if CUSTOM profile is used this attribute must be set.
    """

    def __init__(self,
                 name: str,
                 policy_id: str,
                 self_link: str,
                 min_tls_version: str,
                 profile: str,
                 custom_features: Optional[List[str]]):

        super().__init__(GcpResourceType.GOOGLE_COMPUTE_SSL_POLICY)
        self.name: str = name
        self.policy_id: str = policy_id
        self.self_link: str = self_link
        self.min_tls_version: str = min_tls_version
        self.profile: str = profile
        self.custom_features: Optional[List[str]] = custom_features
        self.with_aliases(policy_id, self_link)

    def get_keys(self) -> List[str]:
        return [self.self_link]

    def get_id(self) -> str:
        return self.policy_id

    def get_name(self) -> Optional[str]:
        return self.name

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False

    @property
    def is_using_secure_ciphers(self) -> bool:
        not_secure_ciphers = ["TLS_RSA_WITH_AES_128_GCM_SHA256", "TLS_RSA_WITH_AES_256_GCM_SHA384", "TLS_RSA_WITH_AES_128_CBC_SHA", "TLS_RSA_WITH_AES_256_CBC_SHA", "TLS_RSA_WITH_3DES_EDE_CBC_SHA"]
        return all(custom_feature not in not_secure_ciphers for custom_feature in self.custom_features) if self.custom_features else True

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-security/sslpolicies/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        return 'Compute SSL Policy Details'

    def to_drift_detection_object(self) -> dict:
        return {"min_tls_version": self.min_tls_version,
                "profile": self.profile,
                "custom_features": self.custom_features}
