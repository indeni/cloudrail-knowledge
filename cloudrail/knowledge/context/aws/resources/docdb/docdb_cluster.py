from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class DocumentDbCluster(AwsResource):
    """
        Attributes:
            cluster_identifier: The ID of the DocDB cluster.
            storage_encrypted: True if the storage is encrypted.
            parameter_group_name: The name of the DB's paramaeter group.
            kms_key_id: If KMS is used, this is the ID of the key.
            kms_data: The actual KMS key in use, if one is used (or None).
            cluster_arn: The ARN of the cluster.
            enabled_cloudwatch_logs_exports: List of log types to export to cloudwatch.
    """

    def __init__(self,
                 cluster_identifier: str,
                 storage_encrypted: bool,
                 parameter_group_name: str,
                 kms_key_id: str,
                 region: str,
                 account: str,
                 cluster_arn: str,
                 enabled_cloudwatch_logs_exports: list):
        super().__init__(account, region, AwsServiceName.AWS_DOCDB_CLUSTER)
        self.cluster_identifier: str = cluster_identifier
        self.storage_encrypted: bool = storage_encrypted
        self.parameter_group_name: str = parameter_group_name
        self.kms_key_id: str = kms_key_id
        self.kms_data: Optional[KmsKey] = None
        self.cluster_arn: str = cluster_arn
        self.enabled_cloudwatch_logs_exports: list = enabled_cloudwatch_logs_exports

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.cluster_identifier]

    def get_name(self) -> str:
        return self.cluster_identifier

    def get_arn(self) -> str:
        return self.cluster_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'DocumentDB Cluster'
        else:
            return 'DocumentDB Clusters'

    def get_cloud_resource_url(self) -> str:
        return '{0}docdb/home?region={1}#cluster-details/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_identifier)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'storage_encrypted': self.storage_encrypted,
                'kms_key_id': self.kms_key_id,
                'enabled_cloudwatch_logs_exports': self.enabled_cloudwatch_logs_exports}
