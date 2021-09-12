from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_vpc_attribute
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class VpcAttributeBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_vpc_attribute(attributes, True)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_VPC


class DefaultVpcAttributeBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_vpc_attribute(attributes, False)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DEFAULT_VPC
