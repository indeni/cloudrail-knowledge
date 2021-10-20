from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


@dataclass
class RdsGlobalClusterRawData:
    source_id: Optional[str] = None


class RdsGlobalCluster(AwsResource):
    """
        Attributes:
            cluster_id: The ID of the cluster.
            encrypted_at_rest: True if the cluster is set to be encrypted at rest.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 cluster_id: str,
                 encrypted_at_rest: bool):
        super().__init__(account, region, AwsServiceName.AWS_RDS_GLOBAL_CLUSTER)
        self.cluster_id: str = cluster_id
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.raw_data: RdsGlobalClusterRawData = RdsGlobalClusterRawData()

    def get_keys(self) -> List[str]:
        pass

    def get_id(self) -> str:
        return self.cluster_id

    def with_raw_data(self, source_id: str) -> RdsGlobalCluster:
        self.raw_data.source_id = source_id
        return self

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'RDS Global Cluster'
        else:
            return 'RDS Global Clusters'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}rds/home?region={1}#database:id={2};is-cluster=false;is-global-cluster=true' \
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'encrypted_at_rest': self.encrypted_at_rest}
