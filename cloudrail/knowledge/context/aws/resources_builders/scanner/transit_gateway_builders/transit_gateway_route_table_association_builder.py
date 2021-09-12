import os

from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_transit_gateway_route_table_association


class TransitGatewayRouteTableAssociationBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-get-transit-gateway-route-table-associations/*'

    def get_section_name(self) -> str:
        return 'Associations'

    def do_build(self, attributes: dict):
        route_table_id = os.path.basename(attributes['FilePath'])
        attributes['RouteTableId'] = route_table_id
        return build_transit_gateway_route_table_association(attributes)
