from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_kms_key


class KmsKeysBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'kms-describe-key/*'

    def get_section_name(self) -> str:
        return 'KeyMetadata'

    def do_build(self, attributes: dict):
        return build_kms_key(attributes)
