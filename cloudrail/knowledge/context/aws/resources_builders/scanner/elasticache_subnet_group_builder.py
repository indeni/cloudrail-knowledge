from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_elasticache_subnet_group


class ElastiCacheSubnetGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'elasticache-describe-cache-subnet-groups.json'

    def get_section_name(self) -> str:
        return 'CacheSubnetGroups'

    def do_build(self, attributes: dict):
        return build_elasticache_subnet_group(attributes)
