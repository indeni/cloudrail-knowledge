from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_code_build_report_group


class CodeBuildReportGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'codebuild-batch-get-report-groups/*'

    def get_section_name(self) -> str:
        return 'reportGroups'

    def do_build(self, attributes: dict):
        return build_code_build_report_group(attributes)
