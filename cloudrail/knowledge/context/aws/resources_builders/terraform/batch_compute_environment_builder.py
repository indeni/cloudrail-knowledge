from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_batch_compute_environment
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class BatchComputeEnvironmentBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_batch_compute_environment(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_BATCH_COMPUTE_ENVIRONMENT
