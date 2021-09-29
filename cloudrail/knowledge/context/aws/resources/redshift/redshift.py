from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.redshift.redshift_logging import RedshiftLogging

from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity


class RedshiftCluster(NetworkEntity, INetworkConfiguration):
    """
        Attributes:
            db_name: The name of the database.
            cluster_identifier: The ID for the cluster.
            port: The port used by the cluster.
            subnet_group_name: The name of the subnet group used by the cluster.
            security_groups: List of IDs of security groups used by the cluster.
            assign_public_ip: True if to assign a public IP to the cluster.
            encrypted: True if the cluster is set to be encrypted at rest.
            security_group_allowing_public_access: A security group that allows access from the internet.
                This value will be None when this resource is not accessible from the internet.
            indirect_public_connection_data: The data that describes that a publicly-accessible resource can access this resource by a security group of this resource.
            logs_config: The logs settings for this cluster, if configured.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 db_name: str,
                 cluster_identifier: str,
                 port: int,
                 subnet_group_name: str,
                 security_groups: List[str],
                 assign_public_ip: bool,
                 encrypted: bool):
        super().__init__(cluster_identifier, account, region, AwsServiceName.AWS_REDSHIFT_CLUSTER)
        self.port: int = port
        self.db_name: str = db_name
        self.subnet_group_name: str = subnet_group_name
        self.network_configuration: NetworkConfiguration = NetworkConfiguration(assign_public_ip, security_groups, None)
        self.encrypted: bool = encrypted
        self.logs_config: Optional[RedshiftLogging] = None
        self.indirect_public_connection_data: Optional[IndirectPublicConnectionData] = None
        self.security_group_allowing_public_access: Optional[SecurityGroup] = None

    @property
    def is_ec2_vpc_platform(self):
        return self.subnet_group_name is not None

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.name]

    def get_name(self) -> str:
        return self.name

    def get_extra_data(self) -> str:
        db_name = 'db_name: {}'.format(self.db_name) if self.db_name else ''
        port = 'port: {}'.format(self.port) if self.port else ''
        return ', '.join([db_name, port])

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [self.network_configuration]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Redshift cluster'
        else:
            return 'Redshift clusters'

    def get_cloud_resource_url(self) -> str:
        return '{0}redshiftv2/home?region={1}#cluster-details?cluster={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
