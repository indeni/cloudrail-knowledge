from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class MainRouteTableAssociation(AwsResource):
    """
        Attributes:
            vpc_id: The VPC the route table is the main one for.
            route_table_id: The ID of the route table that is to be the
                main one for the VPC.
    """

    def __init__(self,
                 vpc_id: str,
                 route_table_id: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_MAIN_ROUTE_TABLE_ASSOCIATION)
        self.route_table_id = route_table_id
        self.vpc_id = vpc_id

    def get_keys(self) -> List[str]:
        return [self.route_table_id, self.vpc_id]

    def get_extra_data(self) -> str:
        route_table_id = 'route_table_id: {}'.format(self.route_table_id) if self.route_table_id else ''
        vpc_id = 'vpc_id: {}'.format(self.vpc_id) if self.vpc_id else ''

        return ', '.join([route_table_id, vpc_id])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Main route table association'
        else:
            return 'Main route table associations'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#RouteTables:routeTableId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.route_table_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'vpc_id': self.vpc_id,
                'route_table_id': self.route_table_id}
