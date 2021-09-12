from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_ecs_task_definition


class EcsTaskDefinitionBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ecs-describe-task-definition/*'

    def get_section_name(self) -> str:
        return 'taskDefinition'

    def do_build(self, attributes: dict):
        return build_ecs_task_definition(attributes)
