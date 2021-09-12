from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_iam_password_policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IamPasswordPolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_password_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_ACCOUNT_PASSWORD_POLICY
