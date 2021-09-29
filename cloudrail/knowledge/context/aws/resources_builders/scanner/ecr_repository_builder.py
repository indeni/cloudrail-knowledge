from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_ecr_repository


class EcrRepositoryBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ecr-describe-repositories.json'

    def get_section_name(self) -> str:
        return 'repositories'

    def do_build(self, attributes: dict):
        return build_ecr_repository(attributes)
