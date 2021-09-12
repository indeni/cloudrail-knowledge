from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.secretsmanager.secrets_manager_secret_policy import SecretsManagerSecretPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class SecretsManagerSecret(AwsResource):
    """
        Attributes:
            sm_name: The name of the owning SageManager.
            arn: The ARN of this secret.
            policy: The resource policy to use with this secret, if any.
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
        self.policy: SecretsManagerSecretPolicy = None
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
