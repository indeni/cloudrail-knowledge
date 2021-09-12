from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_glue_data_catalog_table


class GlueDataCatalogTableBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'glue-get-tables/*'

    def get_section_name(self) -> str:
        return 'TableList'

    def do_build(self, attributes: dict):
        return build_glue_data_catalog_table(attributes)
