from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import EcsTaskDefinition
from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_ecs_task_definition


class EcsTaskDefinitionBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict) -> EcsTaskDefinition:
        return build_ecs_task_definition(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ECS_TASK_DEFINITION
