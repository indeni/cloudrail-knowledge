from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_glacier_vault_policy


class GlacierVaultPolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'glacier-get-vault-access-policy/*'

    def get_section_name(self) -> str:
        return 'policy'

    def do_build(self, attributes: dict):
        return build_glacier_vault_policy(attributes)
