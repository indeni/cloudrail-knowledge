from typing import Dict, List
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationPolicyRoleAttachmentBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> PolicyRoleAttachment:
        policy_role_attachments: List[PolicyRoleAttachment] = []
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        policy_name = properties['PolicyName']
        policy_arn = build_arn('iam', None, account, 'policy', None, policy_name)
        for role in self.get_property(properties, 'Roles', []):
            policy_role_attachments.append(PolicyRoleAttachment(account, policy_arn, role))

        return policy_role_attachments
