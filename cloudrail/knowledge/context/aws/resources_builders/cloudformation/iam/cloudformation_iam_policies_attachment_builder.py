from typing import Dict, List, Optional
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_group_attachment import PolicyGroupAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_user_attachment import PolicyUserAttachment
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationPolicyRoleAttachmentBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_MANAGED_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Optional[PolicyRoleAttachment]:
        properties: dict = cfn_res_attr['Properties']
        if 'Roles' in properties:
            policy_role_attachments: List[PolicyRoleAttachment] = []
            account = cfn_res_attr['account_id']
            policy_name = properties['ManagedPolicyName']
            policy_arn = build_arn('iam', None, account, 'policy', self.get_property(properties, 'Path'), policy_name)
            for role in self.get_property(properties, 'Roles', []):
                policy_role_attachments.append(PolicyRoleAttachment(account, policy_arn, role))

            return policy_role_attachments
        return None


class CloudformationPolicyUserAttachmentBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_MANAGED_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Optional[PolicyUserAttachment]:
        properties: dict = cfn_res_attr['Properties']
        if 'Users' in properties:
            policy_user_attachments: List[PolicyUserAttachment] = []
            account = cfn_res_attr['account_id']
            policy_name = properties['ManagedPolicyName']
            policy_arn = build_arn('iam', None, account, 'policy', self.get_property(properties, 'Path'), policy_name)
            for user in self.get_property(properties, 'Users', []):
                policy_user_attachments.append(PolicyUserAttachment(account, policy_arn, self.create_random_pseudo_identifier(), user))

            return policy_user_attachments
        return None


class CloudformationPolicyGroupAttachmentBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_MANAGED_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Optional[PolicyGroupAttachment]:
        properties: dict = cfn_res_attr['Properties']
        if 'Groups' in properties:
            policy_group_attachments: List[PolicyGroupAttachment] = []
            account = cfn_res_attr['account_id']
            policy_name = properties['ManagedPolicyName']
            policy_arn = build_arn('iam', None, account, 'policy', self.get_property(properties, 'Path'), policy_name)
            for group in self.get_property(properties, 'Groups', []):
                policy_group_attachments.append(PolicyGroupAttachment(account, policy_arn, self.create_random_pseudo_identifier(), group))

            return policy_group_attachments
        return None
