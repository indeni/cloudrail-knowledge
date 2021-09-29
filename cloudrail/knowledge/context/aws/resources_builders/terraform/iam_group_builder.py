from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_iam_group, build_policy_group_attachment, \
    build_group_inline_policy, build_iam_group_membership
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IamGroupBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_GROUP


class PolicyGroupAttachmentBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_policy_group_attachment(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_GROUP_POLICY_ATTACHMENT


class GroupInlinePolicieBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_group_inline_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_GROUP_POLICY


class IamGroupMembershipBuilder(AwsTerraformBuilder):

    def do_build(self, attributes: dict):
        return build_iam_group_membership(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_IAM_GROUP_MEMBERSHIP
