from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_athena_database
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class AthenaDatabaseBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_athena_database(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_ATHENA_DATABASE
