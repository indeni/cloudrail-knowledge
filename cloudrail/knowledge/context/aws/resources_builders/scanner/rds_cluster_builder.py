from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_rds_cluster


class RdsClusterBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'rds-describe-db-clusters.json'

    def get_section_name(self) -> str:
        return 'DBClusters'

    def do_build(self, attributes: dict):
        return build_rds_cluster(attributes)
