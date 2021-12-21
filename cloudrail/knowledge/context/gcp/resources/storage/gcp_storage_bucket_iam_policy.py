from typing import List, Optional
from cloudrail.knowledge.context.gcp.resources.iam.iam_access_policy import GcpIamPolicyType, IamAccessPolicy, GcpIamPolicyBinding


class GcpStorageBucketIamPolicy(IamAccessPolicy):
    """
        Attributes:
            bucket_name: The Storage bucket name this IAM policy is attached to.
            bindings: The list of IAM policy attributes.
    """

    def __init__(self,
                 bucket_name: str,
                 bindings: List[GcpIamPolicyBinding],
                 policy_type: GcpIamPolicyType = GcpIamPolicyType.AUTHORITATIVE):

        super().__init__(bucket_name, bindings)
        self.bucket_name: str = bucket_name
        self.bindings: List[GcpIamPolicyBinding] = bindings
        self.policy_type: GcpIamPolicyType = policy_type
        self.is_default: bool = False

    def get_keys(self) -> List[str]:
        return [self.bucket_name]

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.bucket_name

    def get_name(self) -> Optional[str]:
        return f'IAM policy of {self.bucket_name}'

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/storage/browser/{self.bucket_name};tab=permissions?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Storage Bucket IAM Policy'
        else:
            return 'Storage Bucket IAM policies'

    def to_drift_detection_object(self) -> dict:
        return {}
