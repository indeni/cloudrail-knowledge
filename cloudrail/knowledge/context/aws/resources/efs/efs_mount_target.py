from typing import List, Optional
from dataclasses import dataclass

from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


@dataclass
class MountTargetSecurityGroups:
    security_groups_ids: List[str]
    mount_target_id: str


class EfsMountTarget(NetworkEntity):
    """
        Attributes:
            efs_id: The ID of the EFS the mount target belongs to.
            mount_target_id: The ID of the mount target.
            eni_id: The ID of the elastic network interface the target is using.
            subnet_id: The ID of the subnet the EFS Mount Target is on.
            security_groups_ids: The security groups protecting the target.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 efs_id: str,
                 mount_target_id: str,
                 eni_id: str,
                 subnet_id: str,
                 security_groups_ids: Optional[List[str]]):
        super().__init__(mount_target_id, account, region, AwsServiceName.AWS_EFS_MOUNT_TARGET)
        self.mount_target_id: str = mount_target_id
        self.efs_id: str = efs_id
        self.eni_id: str = eni_id
        self.subnet_id: str = subnet_id
        self.security_groups_ids: Optional[List[str]] = security_groups_ids

    def get_keys(self) -> List[str]:
        return [self.mount_target_id]

    def get_name(self) -> str:
        return f'mount target with id: {self.mount_target_id}'

    def get_arn(self) -> str:
        pass

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'EFS mount target'
        else:
            return 'EFS mount targets'

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        return [NetworkConfiguration(False, self.security_groups_ids, [self.subnet_id])]

    def get_cloud_resource_url(self) -> str:
        return '{0}efs/home?region={1}#/file-systems/{2}?tabId=mounts' \
            .format(self.AWS_CONSOLE_URL, self.region, self.efs_id)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'efs_id': self.efs_id,
                'eni_id': self.eni_id,
                'subnet_id': self.subnet_id,
                'security_groups_ids': self.security_groups_ids}
