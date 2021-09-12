from typing import List, Optional

from cloudrail.knowledge.context.connection import ConnectionInstance
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class NeptuneCluster(ConnectionInstance, AwsResource):
    """
        Attributes:
            cluster_identifier: The identifier of the cluster.
            arn: The ARN of the cluster.
            encrypted_at_rest: True if the cluster is configured to be encrypted
                at rest.
            port: The port the cluster is listening to.
            db_subnet_group_name: The subnet group's name.
            security_group_ids: The IDs of the securiry groups used by the cluster,
                if any.
            cluster_id: The ID of the cluster.
            kms_key: The KMS key used for encryption, if any.
            kms_data: A pointer to the KMS key, if one is used.
            is_in_default_vpc: True if the cluster is in the default VPC.
            cluster_instances: The instances of the cluster.
            cloudwatch_logs_exports: A list of the log types this Neptune cluster is configured to export to Cloudwatch Logs.
    """
    def __init__(self,
                 cluster_identifier: str,
                 arn: str,
                 encrypted_at_rest: bool,
                 region: str,
                 account: str,
                 port: int,
                 db_subnet_group_name: str,
                 security_group_ids: List[str],
                 cluster_id: str,
                 cloudwatch_logs_exports: Optional[list]):
        ConnectionInstance.__init__(self)
        AwsResource.__init__(self, account, region, AwsServiceName.AWS_NEPTUNE_CLUSTER)
        self.cluster_identifier: str = cluster_identifier
        self.arn: str = arn
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.kms_key: str = None
        self.kms_data: Optional[KmsKey] = None
        self.port: int = port
        self.db_subnet_group_name: str = db_subnet_group_name
        self.is_in_default_vpc: bool = db_subnet_group_name is None
        self.cluster_instances: List[NeptuneInstance] = []
        self.security_group_ids: List[str] = security_group_ids
        self.cluster_id: str = cluster_id
        self.cloudwatch_logs_exports: Optional[list] = cloudwatch_logs_exports

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.cluster_identifier

    def get_id(self) -> str:
        return self.cluster_identifier

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Neptune DB Cluster'
        else:
            return 'Neptune DB Clusters'

    def get_cloud_resource_url(self) -> str:
        return '{0}neptune/home?region={1}#database:id={2};is-cluster=true'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_identifier)

    @property
    def is_tagable(self) -> bool:
        return True
