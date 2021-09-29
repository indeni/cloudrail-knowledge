from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_route_table


class RouteTableBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-route-tables.json'

    def get_section_name(self) -> str:
        return 'RouteTables'

    def do_build(self, attributes: dict):
        return build_route_table(attributes)
