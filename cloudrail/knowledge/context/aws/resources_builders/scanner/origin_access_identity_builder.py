from typing import Optional

from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    origin_access_identity_builder


class OriginAccessIdentityBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'cloudfront-list-cloud-front-origin-access-identities.json'

    def get_section_name(self) -> Optional[str]:
        return 'CloudFrontOriginAccessIdentityList'

    def do_build(self, attributes: dict):
        return origin_access_identity_builder(attributes)
