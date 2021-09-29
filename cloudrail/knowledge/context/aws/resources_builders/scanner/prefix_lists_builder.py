from typing import Optional

from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_prefix_lists


class PrefixListsBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-prefix-lists.json'

    def get_section_name(self) -> Optional[str]:
        return None

    def do_build(self, attributes: dict):
        return build_prefix_lists(attributes)
