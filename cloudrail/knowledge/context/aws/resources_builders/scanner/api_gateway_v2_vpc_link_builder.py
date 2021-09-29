from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_api_gateway_v2_vpc_link


class ApiGatewayVpcLinkBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'apigatewayv2-get-vpc-links.json'

    def get_section_name(self) -> str:
        return 'Items'

    def do_build(self, attributes: dict):
        return build_api_gateway_v2_vpc_link(attributes)
