from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.connection import ConnectionInstance
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.utils.tags_utils import filter_tags


class RdsCluster(ConnectionInstance, AwsResource):
    """
        Attributes:
            cluster_id: The ID of the cluster.
            arn: The ARN of the RDS cluster.
            port: The port the cluster is configured to listen to.
            db_subnet_group_name: The name of DB subnet group used.
            security_group_ids: The IDs of the security groups used by this
                database.
            is_in_default_vpc: True if the RDS is in the default VPC.
            encrypted_at_rest: True if the database is configured to be encrypted
                at rest.
            backup_retention_period: Number of days to retain backups.
            engine_type: The Database engine name to be used for this RDS cluster.
            engine_version: The Database engine version to be used for this RDS cluster.
            iam_database_authentication_enabled: An indication whether authentication to the RDS cluster using IAM entities is enabled.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 cluster_id: str,
                 arn: str,
                 port: int,
                 db_subnet_group_name: str,
                 security_group_ids: List[str],
                 encrypted_at_rest: bool,
                 backup_retention_period: int,
                 engine_type: str,
                 engine_version: str,
                 iam_database_authentication_enabled: bool,
                 cloudwatch_logs_exports: Optional[list]):
        ConnectionInstance.__init__(self)
        AwsResource.__init__(self, account, region, AwsServiceName.AWS_RDS_CLUSTER)
        self.cluster_id: str = cluster_id
        self.arn: str = arn
        self.port: int = port
        self.db_subnet_group_name: str = db_subnet_group_name
        self.is_in_default_vpc: bool = db_subnet_group_name is None
        self.cluster_instances: List[RdsInstance] = []
        self.security_group_ids: List[str] = security_group_ids
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.backup_retention_period: int = backup_retention_period
        self.engine_type: str = engine_type
        self.engine_version: str = engine_version
        self.iam_database_authentication_enabled: bool = iam_database_authentication_enabled
        self.cloudwatch_logs_exports: Optional[list] = cloudwatch_logs_exports

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_id(self) -> str:
        return self.cluster_id

    def get_arn(self) -> str:
        return self.arn

    def get_extra_data(self) -> str:
        port = 'port: {}'.format(self.port) if self.port else ''
        db_subnet_group_name = 'db_subnet_group_name: {}'.format(self.db_subnet_group_name) if self.db_subnet_group_name else ''
        return ', '.join([port, db_subnet_group_name])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'RDS DB cluster'
        else:
            return 'RDS DB clusters'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}rds/home?region={1}#database:id={2};is-cluster=true' \
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_id)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'port': self.port,
                'db_subnet_group_name': self.db_subnet_group_name,
                'security_group_ids': self.security_group_ids,
                'encrypted_at_rest': self.encrypted_at_rest,
                'backup_retention_period': self.backup_retention_period,
                'iam_database_authentication_enabled': self.iam_database_authentication_enabled,
                'cloudwatch_logs_exports': self.cloudwatch_logs_exports}
