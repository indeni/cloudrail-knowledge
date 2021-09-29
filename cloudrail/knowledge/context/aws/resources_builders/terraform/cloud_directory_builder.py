from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_directory_service
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudDirectoryBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_directory_service(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DIRECTORY_SERVICE_DIRECTORY
