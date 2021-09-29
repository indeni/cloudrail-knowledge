from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_elasti_cache_replication_group


class ElastiCacheReplicationGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'elasticache-describe-replication-groups.json'

    def get_section_name(self) -> str:
        return 'ReplicationGroups'

    def do_build(self, attributes: dict):
        return build_elasti_cache_replication_group(attributes)
