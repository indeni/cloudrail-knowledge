from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_peering_connection


class PeeringConnectionBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-vpc-peering-connections.json'

    def get_section_name(self) -> str:
        return 'VpcPeeringConnections'

    def do_build(self, attributes: dict):
        peering_connection = build_peering_connection(attributes)
        return peering_connection if peering_connection.status == 'active' else None
