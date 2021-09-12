from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_ami, build_ami_copy, build_ami_from_instance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class AwsAmiBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_ami(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_AMI


class AwsAmiCopyBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_ami_copy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_AMI_COPY


class AwsAmiFromInstanceBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_ami_from_instance(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_AMI_FROM_INSTANCE
