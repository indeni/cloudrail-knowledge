from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_docdb_cluster_parameter_group


class DocDbClusterParameterGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'docdb-describe-db-cluster-parameters/*'

    def get_section_name(self) -> str:
        pass

    def do_build(self, attributes: dict):
        return build_docdb_cluster_parameter_group(attributes)
