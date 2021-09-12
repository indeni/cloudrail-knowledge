from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_emr_cluster


class EmrClusterBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'emr-describe-cluster/*'

    def get_section_name(self) -> str:
        return 'Cluster'

    def do_build(self, attributes: dict):
        return build_emr_cluster(attributes)
