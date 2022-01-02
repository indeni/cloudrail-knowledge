from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_transit_gateway_route
from cloudrail.knowledge.context.environment_context.common_component_builder import extract_attribute_from_file_path


class TransitGatewayRouteBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-search-transit-gateway-routes/*'

    def get_section_name(self) -> str:
        return 'Routes'

    def do_build(self, attributes: dict):
        route_table_id = extract_attribute_from_file_path(attributes['FilePath'],
                                                          ['_Filters', 'TransitGatewayRouteTableId-',
                                                           '_static_filter', '_active_filter'])
        attributes['RouteTableId'] = route_table_id
        return build_transit_gateway_route(attributes)
