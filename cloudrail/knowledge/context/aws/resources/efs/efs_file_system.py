from typing import List

from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElasticFileSystem(PoliciedResource):
    """
        Attributes:
            creation_token: When an EFS is being created, this is used to ensure
                only one EFS is created.
            efs_id: The ID of the EFS.
            arn: The ARN of the EFS.
            encrypted: True if the EFS is encrypted.
    """

    def __init__(self,
                 creation_token: str,
                 efs_id: str,
                 arn: str,
                 encrypted: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_EFS_FILE_SYSTEM)
        self.creation_token: str = creation_token
        self.efs_id: str = efs_id
        self.arn: str = arn
        self.encrypted: bool = encrypted

    def get_keys(self) -> List[str]:
        return [self.efs_id]

    def get_name(self) -> str:
        return self.creation_token

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return '{0}efs/home?region={1}#/file-systems/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.efs_id)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'creation_token': self.creation_token,
                'encrypted': self.encrypted}
