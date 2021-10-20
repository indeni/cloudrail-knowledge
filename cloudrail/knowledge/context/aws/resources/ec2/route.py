from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource

from cloudrail.knowledge.context.aws.resources.ec2.peering_connection import PeeringConnection


class RouteTargetType(str, Enum):
    GATEWAY_ID = 'GatewayId'
    NAT_GATEWAY_ID = 'NatGatewayId'
    INSTANCE_ID = 'InstanceId'
    EGRESS_ONLY_GATEWAY_ID = 'EgressOnlyInternetGatewayId'
    VPC_PEERING_ID = 'VpcPeeringConnectionId'
    TRANSIT_GATEWAY_ID = 'TransitGatewayId'
    NETWORK_INTERFACE_ID = 'NetworkInterfaceId'


class Route(AwsResource):
    """
        Attributes:
            route_table_id: The ID of the routing table the route belongs to.
            target: The target of the route (value depends on type).
            target_type: The type of the route's target.
            destination: The destination subnet defined for the route.
            peering_connection: If hte target is a VPC_PEERING_ID, then this is
                a pointer to the matching connection.
    """

    def __init__(self, route_table_id: str, destination: str, target_type: RouteTargetType,
                 target: str, region: str, account: str):
        super().__init__(account, region, AwsServiceName.AWS_ROUTE)
        self.route_table_id = route_table_id
        self.target = target
        self.target_type = target_type
        self.destination = destination
        self.route_id: str = f'{route_table_id}_{destination}'  # todo - match with cfn stack creation
        self.with_aliases(self.route_id)
        self.peering_connection: Optional[PeeringConnection] = None

    def get_keys(self) -> List[str]:
        return [self.route_table_id, self.destination, self.target_type, self.target]

    def get_extra_data(self) -> str:
        route_table_id = 'route_table_id: {}'.format(self.route_table_id) if self.route_table_id else ''
        target = 'target: {}'.format(self.target) if self.target else ''
        target_type = 'target_type: {}'.format(self.target_type) if self.target_type else ''
        destination = 'destination: {}'.format(self.destination) if self.destination else ''

        return ', '.join([route_table_id, target, target_type, destination])

    def is_internet_gateway_target(self) -> bool:
        return self.get_target_resource_type() == AwsServiceName.AWS_INTERNET_GATEWAY

    def get_target_resource_type(self) -> AwsServiceName:
        target_type: AwsServiceName = AwsServiceName.NONE
        if self.target_type == RouteTargetType.GATEWAY_ID:
            if self.target.startswith("igw-") or self.target.__contains__("aws_internet_gateway."):
                target_type = AwsServiceName.AWS_INTERNET_GATEWAY
            elif self.target.startswith("vpce-") or self.target.__contains__("aws_vpc_endpoint."):
                target_type = AwsServiceName.AWS_VPC_ENDPOINT
            elif self.target.startswith("vgw-") or self.target.__contains__("aws_vpn_gateway."):
                target_type = AwsServiceName.NONE  # todo - don't exist yet
            elif self.target.startswith("tgw-") or self.target.__contains__("aws_ec2_transit_gateway."):
                target_type = AwsServiceName.AWS_TRANSIT_GATEWAY
        elif self.target_type == RouteTargetType.NAT_GATEWAY_ID:
            target_type = AwsServiceName.AWS_NAT_GATEWAY
        elif self.target_type == RouteTargetType.INSTANCE_ID:
            target_type = AwsServiceName.AWS_EC2_INSTANCE
        elif self.target_type == RouteTargetType.EGRESS_ONLY_GATEWAY_ID:
            target_type = AwsServiceName.AWS_EGRESS_ONLY_INTERNET_GATEWAY
        elif self.target_type == RouteTargetType.VPC_PEERING_ID:
            target_type = AwsServiceName.AWS_VPC_PEERING_CONNECTION
        elif self.target_type == RouteTargetType.NETWORK_INTERFACE_ID:
            target_type = AwsServiceName.AWS_NETWORK_INTERFACE
        return target_type

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#RouteTables:routeTableId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.route_table_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.route_id

    def to_drift_detection_object(self) -> dict:
        return {'route_table_id': self.route_table_id,
                'target': self.target,
                'target_type': self.target_type,
                'destination': self.destination}
