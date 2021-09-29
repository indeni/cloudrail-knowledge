from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_s3_public_access_block_settings
from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings import PublicAccessBlockLevel


class PublicAccessBlockSettingsBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return "s3-get-public-access-block/*"

    def get_section_name(self) -> str:
        return "PublicAccessBlockConfiguration"

    def do_build(self, attributes: dict):
        return build_s3_public_access_block_settings(attributes)


class AccountPublicAccessBlockSettingsBuilder(PublicAccessBlockSettingsBuilder):

    def get_file_name(self) -> str:
        return "s3control-get-public-access-block/*"

    def do_build(self, attributes: dict):
        attributes["access_level"] = PublicAccessBlockLevel.ACCOUNT
        return build_s3_public_access_block_settings(attributes)
