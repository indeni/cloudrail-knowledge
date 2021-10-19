from typing import List

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElastiCacheSubnetGroup(AwsResource):
    """
        Attributes:
            subnet_group_name: The name of the subnet group.
            subnet_ids: The IDs of the subnets included in this group.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 subnet_group_name: str,
                 subnet_ids: list):
        super().__init__(account, region, AwsServiceName.AWS_ELASTICACHE_SUBNET_GROUP)
        self.subnet_group_name: str = subnet_group_name
        self.subnet_ids: list = subnet_ids

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.subnet_group_name]

    def get_name(self) -> str:
        return self.subnet_group_name

    def get_arn(self) -> str:
        pass

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ElastiCache subnet group'
        else:
            return 'ElastiCache subnet groups'

    def get_cloud_resource_url(self) -> str:
        return '{0}elasticache/home?region={1}#cache-subnet-groups:names={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.subnet_group_name)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'subnet_group_name': self.subnet_group_name,
                'subnet_ids': self.subnet_ids}
