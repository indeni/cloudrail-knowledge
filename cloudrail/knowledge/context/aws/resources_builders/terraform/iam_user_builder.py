from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_policy_user_attachment, build_iam_user, \
    build_user_inline_policy, build_iam_user_group_membership, build_user_login_profile
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IamUserBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_user(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER


class PolicyUserAttachmentBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_policy_user_attachment(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER_POLICY_ATTACHMENT


class UserInlinePolicieBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_user_inline_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER_POLICY


class IamUserGroupMembershipBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_user_group_membership(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER_GROUP_MEMBERSHIP


class IamUsersLoginProfileBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_user_login_profile(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_USER_LOGIN_PROFILE
