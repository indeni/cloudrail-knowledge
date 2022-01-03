from typing import Callable, Dict, List, Optional
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_group_attachment import PolicyGroupAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_user_attachment import PolicyUserAttachment
from cloudrail.knowledge.context.aws.resources.iam.iam_policy_attachment import IamPolicyAttachment
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentityType
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

class CloudformationIamPolicyAttachmentGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[IamPolicyAttachment]:
        res_properties: dict = cfn_res_attr['Properties']
        return _build_policy_attachments(cfn_res_attr['account_id'], res_properties, self.get_property, self.create_random_pseudo_identifier)


class CloudformationIamPolicyAttachmentRoleBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_ROLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[IamPolicyAttachment]:
        res_properties: dict = cfn_res_attr['Properties']
        return _build_policy_attachments(cfn_res_attr['account_id'], res_properties, self.get_property, self.create_random_pseudo_identifier)


class CloudformationIamPolicyAttachmentUserBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_USER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[IamPolicyAttachment]:
        res_properties: dict = cfn_res_attr['Properties']
        return _build_policy_attachments(cfn_res_attr['account_id'], res_properties, self.get_property, self.create_random_pseudo_identifier)


def _build_policy_attachments(account:str, properties: dict, get_property: Callable, pseudo_id: Callable) -> List[IamPolicyAttachment]:
    iam_policy_attachments: List[IamPolicyAttachment] = []
    users = []
    roles = []
    groups = []
    _update_iam_identity_list(users, properties, IamIdentityType.USER)
    _update_iam_identity_list(roles, properties, IamIdentityType.ROLE)
    _update_iam_identity_list(groups, properties, IamIdentityType.GROUP)
    for policy_arn in get_property(properties, 'ManagedPolicyArns', []):
        iam_policy_attachments.append(IamPolicyAttachment(account=account,
                                                          policy_arn=policy_arn,
                                                          attachment_name=pseudo_id,
                                                          users=users,
                                                          roles=roles,
                                                          groups=groups))
    return iam_policy_attachments

def _update_iam_identity_list(iam_identity_list: list, properties: dict, iam_identity_type: IamIdentityType):
    identity = properties.get(iam_identity_type.value)
    if identity:
        iam_identity_list.append(identity)
