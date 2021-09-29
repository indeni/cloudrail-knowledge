from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_launch_template


class LaunchTemplatesBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-launch-template-versions/*'

    def get_section_name(self) -> str:
        return 'LaunchTemplateVersions'

    def do_build(self, attributes: dict):
        return build_launch_template(attributes)
