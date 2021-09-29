from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_eni_instance


class NetworkInterfaceBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-network-interfaces.json'

    def get_section_name(self) -> str:
        return 'NetworkInterfaces'

    def do_build(self, attributes: dict):
        return build_eni_instance(attributes)
