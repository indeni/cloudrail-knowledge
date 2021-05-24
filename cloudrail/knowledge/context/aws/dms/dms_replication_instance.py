from typing import List, Optional

from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class DmsReplicationInstance(NetworkEntity, INetworkConfiguration):
    """
        Attributes:
            name: The name of the DMS replication instance.
            arn: The ARN of the instance.
            publicly_accessible: True if the DMS is set to be publicly accessible.
            rep_instance_subnet_group_id: Replication instance subnet group ID.
            subnet_ids: The actual subnets the DMS is connected to.
            security_group_ids: The IDs of the security groups the DMS is using.
            is_in_default_vpc: True if the DMS instance is in the default VPC.
            security_group_allowing_public_access: A security group that allows access from the internet.
                This value will be None when this resource is not accessible from the internet.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 arn: str,
                 publicly_accessible: bool,
                 rep_instance_subnet_group_id: str,
                 security_group_ids: List[str]):
        super().__init__(name, account, region, AwsServiceName.AWS_DMS_REPLICATION_INSTANCE)
        self.arn: str = arn
        self.publicly_accessible: bool = publicly_accessible
        self.rep_instance_subnet_group_id: str = rep_instance_subnet_group_id
        self.is_in_default_vpc: bool = rep_instance_subnet_group_id == 'default' or not self.rep_instance_subnet_group_id
        self.security_group_ids: List[str] = security_group_ids
        self.subnet_ids: Optional[List[str]] = None

        self.security_group_allowing_public_access: Optional[SecurityGroup] = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_id(self) -> str:
        return self.rep_instance_subnet_group_id

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [NetworkConfiguration(self.publicly_accessible, self.security_group_ids, self.subnet_ids)]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'DMS replication instance'
        else:
            return 'DMS replication instances'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}dms/v2/home?region={1}#replicationInstanceDetails/{2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    @property
    def is_tagable(self) -> bool:
        return True
