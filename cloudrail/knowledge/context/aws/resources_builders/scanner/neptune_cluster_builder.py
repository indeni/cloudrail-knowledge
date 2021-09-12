from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_neptune_cluster, build_neptune_instance


class NeptuneClusterBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'neptune-describe-db-clusters.json'

    def get_section_name(self) -> str:
        return 'DBClusters'

    def do_build(self, attributes: dict):
        return build_neptune_cluster(attributes)


class NeptuneInstanceBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'neptune-describe-db-instances.json'

    def get_section_name(self) -> str:
        return ''

    def do_build(self, attributes: dict):
        return build_neptune_instance(attributes)
