from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class AthenaDatabase(AwsResource):
    """
        Attributes:
            database_name: The name of the Database.
            bucket: Name of s3 bucket to save the results of the query execution.
            encryption_option: Set if encryption is configured, one of SSE_S3, SSE_KMS, CSE_KMS.
            kms_key_encryption: If the type of encryption is KMS, this would be the KMS key ARN or ID.
    """

    def __init__(self,
                 database_name: str,
                 bucket: str,
                 encryption_option: Optional[str],
                 kms_key_encryption: Optional[str],
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_ATHENA_DATABASE)
        self.database_name: str = database_name
        self.bucket: str = bucket
        self.encryption_option: Optional[str] = encryption_option
        self.kms_key_encryption: Optional[str] = kms_key_encryption

    def get_keys(self) -> List[str]:
        return [self.database_name, self.region, self.account]

    def get_name(self) -> str:
        return self.database_name

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'database_name': self.database_name,
                'bucket': self.bucket,
                'encryption_option': self.encryption_option,
                'kms_key_encryption': self.kms_key_encryption}
