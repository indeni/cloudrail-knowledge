from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route import TransitGatewayRoute
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table_association import TransitGatewayRouteTableAssociation
from cloudrail.knowledge.utils.tags_utils import filter_tags


class TransitGatewayRouteTable(AwsResource):
    """
        Attributes:
            tgw_id: The TGW the route table belongs to.
            route_table_id: The id of the route table.
            associations: A list of route table to TGW associations.
            routes: The routes included in this route table.
    """

    def __init__(self, tgw_id, route_table_id, region, account):
        super().__init__(account, region, AwsServiceName.AWS_TRANSIT_GATEWAY_ROUTE_TABLE)
        self.tgw_id: str = tgw_id
        self.route_table_id: str = route_table_id
        self.associations: List[TransitGatewayRouteTableAssociation] = []
        self.routes: List[TransitGatewayRoute] = []

    def get_keys(self) -> List[str]:
        return [self.route_table_id]

    def get_id(self) -> str:
        return self.route_table_id

    def get_extra_data(self) -> str:
        tgw_id = 'tgw_id: {}'.format(self.tgw_id) if self.tgw_id else ''
        route_table_id = 'route_table_id: {}'.format(self.route_table_id) if self.route_table_id else ''

        return ', '.join([tgw_id, route_table_id])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Transit Gateway Route table'
        else:
            return 'Transit Gateway Route tables'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#TransitGatewayRouteTables:transitGatewayRouteTableId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.route_table_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'tgw_id': self.tgw_id,
                'route_table_id': self.route_table_id}
