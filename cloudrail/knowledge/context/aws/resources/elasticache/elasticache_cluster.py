from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElastiCacheCluster(NetworkEntity):
    """
        Attributes:
            cluster_name: The name of the cluster.
            arn: The ARN of the cluster.
            replication_group_id: The ID of the replication group.
            elasticache_security_group_ids: The IDs of the security groups used by this
                cluster.
            subnet_group_name: The name of the subnet group used by the cluster.
            elasticache_subnet_ids: The IDs of the subnet in the subnet group.
            is_in_default_vpc: True if the ElasticCache cluster is in the
                default VPC.
            snapshot_retention_limit: Number of days for which ElastiCache will retain automatic cache cluster snapshots before deleting them.
            engine: Name of the cache engine to be used for the ElasticCache cluster
    """
    def __init__(self,
                 region: str,
                 account: str,
                 cluster_name: str,
                 arn: str,
                 replication_group_id: Optional[str],
                 elasticache_security_group_ids: Optional[list],
                 snapshot_retention_limit: Optional[int],
                 engine: str,
                 subnet_group_name: Optional[str] = 'default'):
        super().__init__(cluster_name, account, region, AwsServiceName.AWS_ELASTICACHE_CLUSTER)
        self.replication_group_id: str = replication_group_id
        self.cluster_name: str = cluster_name
        self.arn: str = arn
        self.elasticache_security_group_ids: Optional[list] = elasticache_security_group_ids
        self.subnet_group_name: Optional[str] = subnet_group_name
        self.elasticache_subnet_ids: Optional[List[str]] = None
        self.is_in_default_vpc: bool = self.subnet_group_name == 'default'
        self.snapshot_retention_limit: Optional[int] = snapshot_retention_limit
        self.engine: str = engine

    def get_keys(self) -> List[str]:
        return [self.get_arn()]

    def get_name(self) -> str:
        return self.cluster_name

    def get_arn(self) -> str:
        return self.arn

    def get_id(self) -> str:
        return self.replication_group_id

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [NetworkConfiguration(False, self.elasticache_security_group_ids, self.elasticache_subnet_ids)]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ElastiCache Cluster'
        else:
            return 'ElastiCache Clusters'

    def get_cloud_resource_url(self) -> str:
        if self.replication_group_id:
            return '{0}elasticache/home?region={1}#redis-group-nodes:id={2};clusters={3}' \
                .format(self.AWS_CONSOLE_URL, self.region, self.replication_group_id, self.cluster_name)
        else:
            return '{0}elasticache/home?region={1}#redis-nodes:id={2}'\
                .format(self.AWS_CONSOLE_URL, self.region, self.cluster_name)

    @property
    def is_tagable(self) -> bool:
        return True
