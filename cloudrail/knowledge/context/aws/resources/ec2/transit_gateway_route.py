from enum import Enum
from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class TransitGatewayRouteState(Enum):
    ACTIVE = 'active'
    BLACKHOLE = 'blackhole'


class TransitGatewayRouteType(Enum):
    STATIC = "static"
    PROPAGATED = "propagated"


class TransitGatewayRoute(AwsResource):
    """
        Attributes:
            destination_cidr_block: The destination CIDR block the route
                is targeting.
            state: The state of the route (active or blackhole).
            route_type: The type of the route (static or propagated).
            route_table_id: The routing table the route belongs to.
    """

    def __init__(self,
                 destination_cidr_block: str,
                 state: TransitGatewayRouteState,
                 route_type: TransitGatewayRouteType,
                 route_table_id: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_TRANSIT_GATEWAY_ROUTE)
        self.destination_cidr_block: str = destination_cidr_block
        self.state: TransitGatewayRouteState = state
        self.route_type: TransitGatewayRouteType = route_type
        self.route_table_id: str = route_table_id

    def get_keys(self) -> List[str]:
        return [self.route_table_id,
                self.destination_cidr_block,
                self.route_type.value]

    def get_extra_data(self) -> str:
        destination_cidr_block = 'destination_cidr_block: {}'.format(self.destination_cidr_block) if self.destination_cidr_block else ''
        route_table_id = 'route_table_id: {}'.format(self.route_table_id) if self.route_table_id else ''
        return ', '.join([destination_cidr_block, route_table_id])

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#TransitGatewayRouteTables:transitGatewayRouteTableId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.route_table_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'destination_cidr_block': self.destination_cidr_block,
                'state': self.state.value,
                'route_type': self.route_type.value,
                'route_table_id': self.route_table_id}
