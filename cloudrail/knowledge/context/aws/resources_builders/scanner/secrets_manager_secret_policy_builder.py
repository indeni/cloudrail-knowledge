from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_secrets_manager_secret_policy


class SecretsManagerSecretPolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'secretsmanager-get-resource-policy/*'

    def get_section_name(self) -> str:
        return ''

    def do_build(self, attributes: dict):
        return build_secrets_manager_secret_policy(attributes)
