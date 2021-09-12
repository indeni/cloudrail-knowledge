from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_iam_role, \
    build_policy_role_attachment, build_role_inline_policy, build_iam_instance_profile, build_iam_role_nested_policy, build_iam_assume_role_policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IamRoleBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_role(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_ROLE


class PolicyRoleAttachmentBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_policy_role_attachment(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_ROLE_POLICY_ATTACHMENT


class RoleInlinePolicieBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_role_inline_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_ROLE_POLICY


class IamInstanceProfileBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_instance_profile(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_INSTANCE_PROFILE


class RoleInlineNestedPolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_role_nested_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_ROLE


class AssumeRolePolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_assume_role_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_ROLE
