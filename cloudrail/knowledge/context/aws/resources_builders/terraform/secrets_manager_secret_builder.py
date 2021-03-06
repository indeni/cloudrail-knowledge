from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_secrets_manager_secret
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SecretsManagerSecretBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_secrets_manager_secret(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_SECRETSMANAGER_SECRET
