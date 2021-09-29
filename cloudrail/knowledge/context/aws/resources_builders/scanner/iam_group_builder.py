from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder \
    import build_iam_group, build_iam_group_inline_policies, build_policy_group_attachments


class IamGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'GroupDetailList'

    def do_build(self, attributes: dict):
        return build_iam_group(attributes)


class IamGroupInlinePoliciesBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'GroupDetailList'

    def do_build(self, attributes: dict):
        return build_iam_group_inline_policies(attributes)


class IamPolicyGroupAttachmentBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'iam-get-account-authorization-details.json'

    def get_section_name(self) -> str:
        return 'GroupDetailList'

    def do_build(self, attributes: dict):
        return build_policy_group_attachments(attributes)
