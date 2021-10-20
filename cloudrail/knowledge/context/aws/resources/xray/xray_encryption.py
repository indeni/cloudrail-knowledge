from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class XrayEncryption(AwsResource):
    """
        Attributes:
            key_id: The ID of the KMS key used to encrypt X-Ray data, if any
                is used.
            kms_data: A reference to KmsKey based on the kms_id provided.
    """
    def __init__(self,
                 key_id: Optional[str],
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_XRAY_ENCRYPTION_CONFIG)
        self.key_id: Optional[str] = key_id
        self.kms_data: KmsKey = None

    def get_keys(self) -> List[str]:
        return [self.account, self.region]

    def get_type(self, is_plural: bool = False) -> str:
        return 'X-Ray encryption'

    def get_cloud_resource_url(self) -> str:
        return '{0}xray/home?region={1}#/encryption-configuration'\
            .format(self.AWS_CONSOLE_URL, self.region)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'kms_id': self.key_id}
