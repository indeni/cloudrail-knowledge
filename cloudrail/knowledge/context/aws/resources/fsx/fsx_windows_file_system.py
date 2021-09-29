from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class FsxWindowsFileSystem(AwsResource):
    """
        Attributes:
            fsx_windows_file_system_id: The ID of this Fsx Windows File System.
            kms_key_id: The ARN of the KMS key used for encryption.
            kms_data: The actual KMS key data used for encryption.
            arn: This resource's ARN.
    """

    def __init__(self,
                 region: str,
                 account: str,
                 fsx_windows_file_system_id: Optional[str],
                 kms_key_id: str,
                 arn: str):
        super().__init__(account, region, AwsServiceName.AWS_FSX_WINDOWS_FILE_SYSTEM)
        self.fsx_windows_file_system_id: str = fsx_windows_file_system_id
        self.kms_key_id: Optional[str] = kms_key_id
        self.arn: str = arn
        self.kms_data: Optional[KmsKey] = None
        self.with_aliases(fsx_windows_file_system_id)

    def get_keys(self) -> List[str]:
        return [self.fsx_windows_file_system_id]

    def get_type(self, is_plural: bool = False) -> str:
        return 'FSx Windows File System' + 's' if is_plural else ''

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return f'https://{self.region}.console.aws.amazon.com/fsx/home?region={self.region}#file-system-details/{self.fsx_windows_file_system_id}'

    def get_id(self) -> str:
        return self.fsx_windows_file_system_id

    @property
    def is_tagable(self) -> bool:
        return True
