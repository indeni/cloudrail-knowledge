from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass

from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster_parameter import DocDbClusterParameter
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


@dataclass
class DocDbClusterParameterGroupRawData:
    """
        An internal raw class, you may ignore this.
    """
    source_id: Optional[str] = None


class DocDbClusterParameterGroup(AwsResource):
    """
        Attributes:
            group_name: The name of the group.
            parameters: The parameters in the group.
            group_arn: The ARN of the group.
    """
    def __init__(self,
                 parameters: List[DocDbClusterParameter],
                 group_name: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_DOCDB_CLUSTER_PARAMETER_GROUP)
        self.parameters: List[DocDbClusterParameter] = parameters
        self.group_name: str = group_name
        self.raw_data: DocDbClusterParameterGroupRawData = DocDbClusterParameterGroupRawData()
        if self.account:
            self.group_arn: str = f'arn:aws:rds:{self.region}:{self.account}:cluster-pg:{self.group_name}'
        else:
            self.arn = None

    def get_keys(self) -> List[str]:
        return [self.group_name, self.account, self.region]

    def with_raw_data(self, source_id: str) -> DocDbClusterParameterGroup:
        self.raw_data.source_id = source_id
        return self

    def get_arn(self) -> str:
        return self.group_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'DocumentDB Cluster Parameter Group'
        else:
            return 'DocumentDB Cluster Parameter Groups'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}docdb/home?region={1}#parameterGroup-details/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.group_name)

    @property
    def is_tagable(self) -> bool:
        return True
