from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_xray_encryption
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class XrayEncryptionBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_xray_encryption(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_XRAY_ENCRYPTION_CONFIG
