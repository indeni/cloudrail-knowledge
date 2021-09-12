from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_xray_encryption


class XrayEncryptionBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'xray-get-encryption-config.json'

    def get_section_name(self) -> str:
        return 'EncryptionConfig'

    def do_build(self, attributes: dict):
        return build_xray_encryption(attributes)
