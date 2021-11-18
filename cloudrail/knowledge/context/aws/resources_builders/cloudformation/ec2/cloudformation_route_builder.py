from typing import Dict
from cloudrail.knowledge.context.aws.resources.ec2.route import Route, RouteTargetType
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationRouteBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ROUTE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Route:
        properties: dict = cfn_res_attr['Properties']
        cidr = self.get_property(properties, 'DestinationCidrBlock') or self.get_property(properties, 'DestinationIpv6CidrBlock')
        target_type = None
        target = None
        if 'GatewayId' in properties:
            target_type = RouteTargetType.GATEWAY_ID
            target = self.get_property(properties, 'GatewayId')
        elif 'NatGatewayId' in properties:
            target_type = RouteTargetType.NAT_GATEWAY_ID
            target = self.get_property(properties, 'NatGatewayId')
        elif 'InstanceId' in properties:
            target_type = RouteTargetType.INSTANCE_ID
            target = self.get_property(properties, 'InstanceId')
        elif 'EgressOnlyInternetGatewayId' in properties:
            target_type = RouteTargetType.EGRESS_ONLY_GATEWAY_ID
            target = self.get_property(properties, 'EgressOnlyInternetGatewayId')
        elif 'TransitGatewayId' in properties:
            target_type = RouteTargetType.TRANSIT_GATEWAY_ID
            target = self.get_property(properties, 'TransitGatewayId')
        elif 'VpcPeeringConnectionId' in properties:
            target_type = RouteTargetType.VPC_PEERING_ID
            target = self.get_property(properties, 'VpcPeeringConnectionId')

        return Route(route_table_id=self.get_property(properties, 'RouteTableId'),
                     destination=cidr,
                     target_type=target_type,
                     target=target,
                     region=cfn_res_attr['region'],
                     account=cfn_res_attr['account_id'])
