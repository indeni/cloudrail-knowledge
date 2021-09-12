from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_workspaces_directory


class WorkspacesDirectoryBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'workspaces-describe-workspace-directories.json'

    def get_section_name(self) -> str:
        return 'Directories'

    def do_build(self, attributes: dict):
        return build_workspaces_directory(attributes)
