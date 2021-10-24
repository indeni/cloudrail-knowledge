from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SecretsManagerSecret(PoliciedResource):
    """
        Attributes:
            sm_name: The name of the owning SageManager.
            arn: The ARN of this secret.
            kms_key: The KMS key ID to use to encrypt this secret, if one is used.
            kms_data: The actual KmsKey object referenced by the KMS ID.
    """
    def __init__(self,
                 sm_name: str,
                 arn: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_SECRETSMANAGER_SECRET)
        self.sm_name: str = sm_name
        self.arn: str = arn
        self.kms_key: str = None
        self.kms_data: Optional[KmsKey] = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.sm_name

    def get_cloud_resource_url(self) -> str:
        return '{0}secretsmanager/home?region={1}#!/secret?name={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.sm_name)

    def get_arn(self) -> str:
        return self.arn

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'sm_name': self.sm_name,
                'kms_key': self.kms_key}
