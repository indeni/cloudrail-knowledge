from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_glacier_vault_policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlacierVaultPolicyBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_glacier_vault_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_GLACIER_VAULT
