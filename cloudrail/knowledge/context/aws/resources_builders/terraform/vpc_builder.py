from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_vpc, \
    build_vpc_endpoint
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class VpcBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_vpc(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_VPC


class VpcEndpointBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_vpc_endpoint(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_VPC_ENDPOINT
