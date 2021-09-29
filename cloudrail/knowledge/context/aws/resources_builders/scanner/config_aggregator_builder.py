from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_config_aggregator


class ConfigAggregatorBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'config-describe-configuration-aggregators.json'

    def get_section_name(self) -> str:
        return 'ConfigurationAggregators'

    def do_build(self, attributes: dict):
        return build_config_aggregator(attributes)
