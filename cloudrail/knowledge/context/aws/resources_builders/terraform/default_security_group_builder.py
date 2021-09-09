from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_security_group
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class DefaultSecurityGroupBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_security_group(attributes, True)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DEFAULT_SECURITY_GROUP
