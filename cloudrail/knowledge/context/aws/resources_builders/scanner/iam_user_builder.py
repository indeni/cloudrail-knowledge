from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder \
    import build_iam_user, build_iam_user_inline_policies, \
    build_policy_user_attachments, build_user_group_membership, build_user_login_profile


class IamUserBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'UserDetailList'

    def do_build(self, attributes: dict):
        return build_iam_user(attributes)


class IamUserInlinePoliciesBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'UserDetailList'

    def do_build(self, attributes: dict):
        return build_iam_user_inline_policies(attributes)


class IamPolicyUserAttachmentBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'UserDetailList'

    def do_build(self, attributes: dict):
        return build_policy_user_attachments(attributes)


class IamUserGroupMembershipBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'UserDetailList'

    def do_build(self, attributes: dict):
        return build_user_group_membership(attributes)

class IamUsersLoginProfileBuilder(BaseAwsScannerBuilder):
    def get_file_name(self) -> str:
        return 'iam-get-login-profile/*'

    def get_section_name(self) -> str:
        return 'LoginProfile'

    def do_build(self, attributes: dict):
        return build_user_login_profile(attributes)
