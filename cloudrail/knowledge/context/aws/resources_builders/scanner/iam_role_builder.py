from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_iam_role, \
    build_policy_role_attachments, build_iam_role_inline_policies, build_iam_instance_profile, build_iam_assume_role_policy, build_iam_role_last_used


class IamRoleInlinePoliciesBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'RoleDetailList'

    def do_build(self, attributes: dict):
        return build_iam_role_inline_policies(attributes)


class IamRoleBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'RoleDetailList'

    def do_build(self, attributes: dict):
        return build_iam_role(attributes)


class IamPolicyRoleAttachmentBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'RoleDetailList'

    def do_build(self, attributes: dict):
        return build_policy_role_attachments(attributes)


class IamInstanceProfileBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'RoleDetailList'

    def do_build(self, attributes: dict):
        return build_iam_instance_profile(attributes)


class AssumeRolePolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'RoleDetailList'

    def do_build(self, attributes: dict):
        return build_iam_assume_role_policy(attributes)


class RoleLastUsedBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'RoleDetailList'

    def do_build(self, attributes: dict):
        return build_iam_role_last_used(attributes)
