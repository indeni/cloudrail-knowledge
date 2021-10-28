from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route import TransitGatewayRoute, TransitGatewayRouteState, TransitGatewayRouteType
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table import TransitGatewayRouteTable
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table_association import TransitGatewayRouteTableAssociation
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationTransitGatewayRouteTableBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.TRANSIT_GATEWAY_ROUTE_TABLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> TransitGatewayRouteTable:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account_id = cfn_res_attr['account_id']
        return TransitGatewayRouteTable(self.get_property(properties, 'TransitGatewayId'),
                                        self.get_resource_id(cfn_res_attr),
                                        region,
                                        account_id)


class CloudformationTransitGatewayRouteTableAssociationBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.TRANSIT_GATEWAY_ROUTE_TABLE_ASSOCIATION, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> TransitGatewayRouteTableAssociation:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account_id = cfn_res_attr['account_id']
        return TransitGatewayRouteTableAssociation(self.get_property(properties, 'TransitGatewayAttachmentId'),
                                                   self.get_property(properties, 'RouteTableId'),
                                                   region,
                                                   account_id)


class CloudformationTransitGatewayRouteBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.TRANSIT_GATEWAY_ROUTE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> TransitGatewayRoute:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account_id = cfn_res_attr['account_id']
        destination_cidr_block = self.get_property(properties, 'DestinationCidrBlock')
        state = TransitGatewayRouteState.BLACKHOLE if self.get_property(properties, 'Blackhole') else TransitGatewayRouteState.ACTIVE
        route_table_id = self.get_property(properties, 'TransitGatewayRouteTableId')
        return TransitGatewayRoute(destination_cidr_block,
                                   state,
                                   TransitGatewayRouteType.STATIC,
                                   route_table_id,
                                   region,
                                   account_id)
