from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_transit_gateway_vpc_attachment


class TransitGatewayVpcAttachmentsBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-transit-gateway-vpc-attachments.json'

    def get_section_name(self) -> str:
        return 'TransitGatewayVpcAttachments'

    def do_build(self, attributes: dict):
        return build_transit_gateway_vpc_attachment(attributes)
