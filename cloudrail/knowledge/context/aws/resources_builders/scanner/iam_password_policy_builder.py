from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_iam_password_policy


class IamPasswordPolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-password-policy.json'

    def get_section_name(self) -> str:
        return 'PasswordPolicy'

    def do_build(self, attributes: dict):
        return build_iam_password_policy(attributes)
