from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_managed_policy


class IamPolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'Policies'

    def do_build(self, attributes: dict):
        return build_managed_policy(attributes)
