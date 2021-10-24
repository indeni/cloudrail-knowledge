from typing import List

from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.kms.kms_alias import KmsAlias
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class KmsKey(PoliciedResource):
    """
        Attributes:
            key_id: The ID of the key.
            arn: The ARN of the key.
            key_manager: The Key Manager of this key (customer, or AWS).
            alias_data: The key's alias, if any.
    """

    def __init__(self,
                 key_id: str,
                 arn: str,
                 key_manager: KeyManager,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_KMS_KEY)
        self.key_id: str = key_id
        self.arn: str = arn
        self.key_manager: KeyManager = key_manager
        self.alias_data: KmsAlias = None

    def get_keys(self) -> List[str]:
        return [self.key_id]

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'KMS key'
        else:
            return 'KMS keys'

    def get_cloud_resource_url(self) -> str:
        if self.key_manager == KeyManager.CUSTOMER:
            return '{0}kms/home?region={1}#/kms/keys/{2}' \
                .format(self.AWS_CONSOLE_URL, self.region, self.key_id)
        else:
            return '{0}kms/home?region={1}#/kms/defaultKeys/{2}' \
                .format(self.AWS_CONSOLE_URL, self.region, self.key_id)

    @property
    def is_tagable(self) -> bool:
        return True

    def get_id(self) -> str:
        return self.key_id

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'key_manager': self.key_manager.value}
