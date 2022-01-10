from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.utils.tags_utils import filter_tags


class RdsInstance(NetworkEntity, INetworkConfiguration):
    """
        Attributes:
            name: The name of the instance.
            arn: The ARN of the instance.
            port: The port the instance is listening on.
            publicly_accessible: True if the database is configured to have
                a public IP address.
            db_subnet_group_name: The name of the SB subnet group.
            security_group_ids: The IDs of the security groups in use
                with the instance.
            db_cluster_id: The cluster ID, if this instance is part of a cluster,
                or None otherwise.
            instance_id: The RDS instance ID, if this instance is a standalone DB,
                or None otherwise.
            encrypted_at_rest: True is encryption at rest is enabled.
            performance_insights_enabled: True if performance insights is enabled.
            performance_insights_kms_key: The ARN of the KMS Key used to encrypt
                the performance insights, if any is used.
            performance_insights_kms_data: The actual KMS Key object, if a KMS key
                is used to encrypt performance insights.
            security_group_allowing_public_access: A security group that allows access from the internet.
                This value will be None when this resource is not accessible from the internet.
            indirect_public_connection_data: The data that describes that a publicly-accessible resource can access this resource by a security group of this resource.
            backup_retention_period: Number of days to retain backups.
            engine_type: The Database engine name to be used for this RDS instance.
            engine_version: The Database engine version to be used for this RDS instance.
            iam_database_authentication_enabled: An indication whether authentication to the RDS instance using IAM entities is enabled.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 arn: str,
                 port: int,
                 publicly_accessible: bool,
                 db_subnet_group_name: str,
                 security_group_ids: List[str],
                 db_cluster_id: Optional[str],
                 encrypted_at_rest: bool,
                 performance_insights_enabled: bool,
                 performance_insights_kms_key: Optional[str],
                 engine_type: str,
                 engine_version: str,
                 instance_id: Optional[str]):
        super().__init__(name, account, region, AwsServiceName.AWS_RDS_CLUSTER_INSTANCE)
        self.arn: str = arn
        self.port: int = port
        self.publicly_accessible: bool = publicly_accessible
        self.security_group_ids: List[str] = security_group_ids
        self.db_subnet_group_name: str = db_subnet_group_name
        self.is_in_default_vpc: bool = db_subnet_group_name is None or db_subnet_group_name == 'default'
        self.network_configuration: NetworkConfiguration = NetworkConfiguration(publicly_accessible, security_group_ids, None)
        self.db_cluster_id: Optional[str] = db_cluster_id
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.performance_insights_kms_key: Optional[str] = performance_insights_kms_key
        self.performance_insights_enabled: bool = performance_insights_enabled
        self.performance_insights_kms_data: Optional[KmsKey] = None
        self.backup_retention_period: Optional[int] = None
        self.engine_type: str = engine_type
        self.engine_version: str = engine_version
        self.instance_id: Optional[str] = instance_id
        self.iam_database_authentication_enabled: Optional[bool] = None
        self.cloudwatch_logs_exports: Optional[list] = None
        self.indirect_public_connection_data: Optional[IndirectPublicConnectionData] = None
        self.security_group_allowing_public_access: Optional[SecurityGroup] = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_cfn_resource_id(self):
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_extra_data(self) -> str:
        port = 'port: {}'.format(self.port) if self.port else ''
        db_subnet_group_name = 'db_subnet_group_name: {}'.format(self.db_subnet_group_name) if self.db_subnet_group_name else ''

        return ', '.join([port, db_subnet_group_name])

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [self.network_configuration]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'RDS Instance'
        else:
            return 'RDS Instances'

    def get_cloud_resource_url(self) -> Optional[str]:
        if self.db_cluster_id:
            return '{0}rds/home?region={1}#database:id={2};is-cluster=true'\
                .format(self.AWS_CONSOLE_URL, self.region, self.db_cluster_id)
        else:
            return '{0}rds/home?region={1}#database:id={2};is-cluster=false'\
                .format(self.AWS_CONSOLE_URL, self.region, self.instance_id)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'name': self.name,
                'port': self.port,
                'publicly_accessible': self.network_configuration.assign_public_ip,
                'security_group_ids': self.network_configuration.security_groups_ids,
                'db_cluster_id': self.db_cluster_id,
                'encrypted_at_rest': self.encrypted_at_rest,
                'performance_insights_enabled': self.performance_insights_enabled,
                'iam_database_authentication_enabled': self.iam_database_authentication_enabled,
                'cloudwatch_logs_exports': self.cloudwatch_logs_exports}
