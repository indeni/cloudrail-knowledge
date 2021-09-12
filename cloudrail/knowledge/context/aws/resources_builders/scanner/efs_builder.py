from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_efs


class EfsBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'efs-describe-file-systems.json'

    def get_section_name(self) -> str:
        return 'FileSystems'

    def do_build(self, attributes: dict):
        return build_efs(attributes)
