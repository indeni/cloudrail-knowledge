from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_ecs_cluster


class EcsClusterBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ecs-describe-clusters/*'

    def get_section_name(self) -> str:
        return 'clusters'

    def do_build(self, attributes: dict):
        return build_ecs_cluster(attributes)
