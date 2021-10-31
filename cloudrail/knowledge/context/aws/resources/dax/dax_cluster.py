from typing import List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class DaxCluster(AwsResource):
    """
        Attributes:
            cluster_name: The name of the DAX cluster.
            server_side_encryption: True if SSE is enabled.
            cluster_arn: The ARN of the cluster.
    """

    def __init__(self,
                 cluster_name: str,
                 server_side_encryption: bool,
                 cluster_arn: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_DAX_CLUSTER)
        self.cluster_name: str = cluster_name
        self.with_aliases(self.cluster_name)
        self.server_side_encryption: bool = server_side_encryption
        self.cluster_arn: str = cluster_arn

    def get_keys(self) -> List[str]:
        return [self.cluster_arn]

    def get_name(self) -> str:
        return self.cluster_name

    def get_id(self) -> str:
        return self.cluster_name

    def get_arn(self) -> str:
        return self.cluster_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'DynamoDB DAX cluster'
        else:
            return 'DynamoDB DAX clusters'

    def get_cloud_resource_url(self) -> str:
        return '{0}dynamodb/home?region={1}#cache-cluster:selected={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_name)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'cluster_name': self.cluster_name,
                'server_side_encryption': self.server_side_encryption,
                'cluster_arn': self.cluster_arn}
