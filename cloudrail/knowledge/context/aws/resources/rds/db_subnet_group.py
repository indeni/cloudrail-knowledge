from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class DbSubnetGroup(AwsResource):
    """
        Attributes:
            name: The name of the subnet group.
            subnet_ids: The IDs of the subnets in the group.
            db_subnet_group_arn: The ARN of the subnet group.
    """
    def __init__(self, name: str, subnet_ids: List[str], region: str, account: str, db_subnet_group_arn: str):
        super().__init__(account, region, AwsServiceName.AWS_DB_SUBNET_GROUP)
        self.name: str = name
        self.subnet_ids: List[str] = subnet_ids
        self.db_subnet_group_arn: str = db_subnet_group_arn

    def get_keys(self) -> List[str]:
        return [self.name]

    def get_arn(self) -> str:
        return self.db_subnet_group_arn

    def get_extra_data(self) -> str:
        subnet_ids = 'subnet_ids: {}'.format(self.subnet_ids) if self.subnet_ids else ''
        return ', '.join([subnet_ids])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'DB subnet group'
        else:
            return 'DB subnet groups'

    def get_cloud_resource_url(self) -> str:
        return '{0}rds/home?region={1}#db-subnet-group:id={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    @property
    def is_tagable(self) -> bool:
        return True
