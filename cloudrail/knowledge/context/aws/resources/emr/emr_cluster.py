from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class EmrCluster(NetworkEntity):
    """
    Attributes:
        account: The account ID in which this resource operates.
        region: The region name in which this resource operates.
        cluster_name: The EMR cluster resource name.
        arn: The ARN of the EMR cluster resource.
        cluster_id: The ID of the EMR cluster resource.
        vpc_config: Networking information used by the resource.
        master_sg_id: The ID of the master security group used for the EMR cluster.
        slave_sg_id: The ID of the slave security group used for the EMR cluster.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 cluster_name: str,
                 cluster_id: str,
                 arn: str,
                 vpc_config: NetworkConfiguration,
                 master_sg_id: str,
                 slave_sg_id: str):
        super().__init__(cluster_name, account, region, AwsServiceName.AWS_EMR_CLUSTER)
        self.cluster_name: str = cluster_name
        self.cluster_id: str = cluster_id
        self.arn: str = arn
        self.master_sg_id: str = master_sg_id
        self.slave_sg_id: str = slave_sg_id
        self.vpc_config: Optional[NetworkConfiguration] = vpc_config

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.cluster_name

    def get_arn(self) -> str:
        return self.arn

    def get_id(self) -> str:
        return self.cluster_id

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        if self.vpc_config:
            return [NetworkConfiguration(self.vpc_config.assign_public_ip,
                                         self.vpc_config.security_groups_ids,
                                         self.vpc_config.subnet_list_ids)]
        else:
            return []

    def get_cloud_resource_url(self) -> str:
        return '{0}elasticmapreduce/home?region={1}#cluster-details:{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_id)

    @property
    def is_tagable(self) -> bool:
        return True
