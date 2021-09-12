from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_network_acl


class NetworkAclBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-network-acls.json'

    def get_section_name(self) -> str:
        return 'NetworkAcls'

    def do_build(self, attributes: dict):
        return build_network_acl(attributes)
