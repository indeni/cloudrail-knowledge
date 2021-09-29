from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_elastic_search_domain


class ElasticSearchDomainBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'es-describe-elasticsearch-domains/*'

    def get_section_name(self) -> str:
        return 'DomainStatusList'

    def do_build(self, attributes: dict):
        return build_elastic_search_domain(attributes)
