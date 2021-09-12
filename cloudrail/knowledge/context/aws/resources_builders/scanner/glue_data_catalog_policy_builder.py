from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_glue_data_catalog_policy


class GlueDataCatalogPolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'glue-get-resource-policy.json'

    def get_section_name(self) -> str:
        return ''

    def do_build(self, attributes: dict):
        return build_glue_data_catalog_policy(attributes)
