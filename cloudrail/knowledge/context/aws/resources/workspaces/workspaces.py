from typing import List
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class Workspace(AwsResource):
    """
        Attributes:
            workspace_id: The ID of this workspace.
            root_encryption_enabled: True if root encryption is enabled.
            user_encryption_enabled: True if user encryption is enabled.
            volume_encryption_key: The ID of the KMS key used to encrypt the
                volume, if any.
            keys_data: A reference to KmsKey based on the kms_key provided.
    """
    def __init__(self,
                 region: str,
                 account: str,
                 workspace_id: str,
                 root_encryption_enabled: bool,
                 user_encryption_enabled: bool,
                 volume_encryption_key: str):
        super().__init__(account, region, AwsServiceName.AWS_WORKSPACES_WORKSPACE)
        self.workspace_id: str = workspace_id
        self.root_encryption_enabled: bool = root_encryption_enabled
        self.user_encryption_enabled: bool = user_encryption_enabled
        self.volume_encryption_key: str = volume_encryption_key
        self.keys_data: KmsKey = None
        if self.account:
            self.arn: str = f'arn:aws:workspaces:{self.region}:{self.account}:workspace/{self.workspace_id}'
        else:
            self.arn = None

    def get_keys(self) -> List[str]:
        return [self.workspace_id]

    def get_id(self) -> str:
        return self.workspace_id

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return '{0}workspaces/home?region={1}#listworkspaces:search={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.workspace_id)

    @property
    def is_tagable(self) -> bool:
        return True
