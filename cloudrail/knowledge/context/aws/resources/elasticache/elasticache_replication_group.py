from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElastiCacheReplicationGroup(NetworkEntity):
    """
        Attributes:
            replication_group_id: The ID of this replication group.
            encrypted_at_rest: True if the group is configured to encrypt at rest.
            encrypted_in_transit: True if this group is configured to encrypt in transit.
            subnet_group_name: The name of the subnet group associated with this replication group.
            elasticache_subnet_ids: The IDs of the subnet from the subnet group.
            elasticache_security_group_ids: The security group IDs used by the cluster.
            is_in_default_vpc: True if this group is in the default VPC.
    """

    def __init__(self,
                 replication_group_id: str,
                 encrypted_at_rest: bool,
                 encrypted_in_transit: bool,
                 region: str,
                 account: str):
        super().__init__(replication_group_id, account, region, AwsServiceName.AWS_ELASTICACHE_REPLICATION_GROUP)
        self.replication_group_id: str = replication_group_id
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.encrypted_in_transit: bool = encrypted_in_transit
        self.subnet_group_name: Optional[str] = None
        self.elasticache_security_group_ids: Optional[list] = None
        self.is_in_default_vpc: bool = True
        self.elasticache_subnet_ids: Optional[List[str]] = None

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.replication_group_id]

    def get_name(self) -> str:
        return self.replication_group_id

    def get_id(self) -> str:
        return self.replication_group_id

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [NetworkConfiguration(False, self.elasticache_security_group_ids, self.elasticache_subnet_ids)]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ElastiCache Replication Group'
        else:
            return 'ElastiCache Replication Groups'

    def get_cloud_resource_url(self) -> str:
        return '{0}elasticache/home?region={1}#redis-group-nodes:id={2};clusters'\
            .format(self.AWS_CONSOLE_URL, self.region, self.replication_group_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'replication_group_id': self.replication_group_id,
                'encrypted_at_rest': self.encrypted_at_rest,
                'encrypted_in_transit': self.encrypted_in_transit}
