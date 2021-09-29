from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.ds.directory_service import DirectoryService
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class WorkspaceDirectory(NetworkEntity):
    """
        Attributes:
            directory_id: The ID of the Workspace Directory.
            subnet_ids: A list of IDs of subnets used by the directory, if any.
            security_group_ids: A list of IDs of security groups used by the directory.
            workspace_security_groups: The actual security groups referenced by the IDs
                in security_group_ids.
            cloud_directory: A reference to the DirectoryService this Workspace connects to.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 directory_id: str,
                 subnet_ids: Optional[list],
                 security_group_ids: list):
        super().__init__(directory_id, account, region, AwsServiceName.AWS_WORKSPACES_DIRECTORY)
        self.directory_id: str = directory_id
        self.subnet_ids: Optional[list] = subnet_ids
        self.security_group_ids: list = security_group_ids
        if self.account:
            self.arn: str = f'arn:aws:workspaces:{self.region}:{self.account}:directory/{self.directory_id}'
        else:
            self.arn = None
        self.workspace_security_groups: List[SecurityGroup] = []
        self.cloud_directory: DirectoryService = None

    def get_keys(self) -> List[str]:
        return [self.directory_id]

    def get_id(self) -> str:
        return self.directory_id

    def get_arn(self) -> str:
        return self.arn

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [NetworkConfiguration(False, self.security_group_ids, self.subnet_ids)]

    def get_cloud_resource_url(self) -> str:
        return '{0}workspaces/home?region={1}#directories:directories'\
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
