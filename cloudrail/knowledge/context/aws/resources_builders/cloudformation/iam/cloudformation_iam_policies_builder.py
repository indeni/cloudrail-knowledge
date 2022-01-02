from typing import Callable, List, Dict, Optional

from cloudrail.knowledge.context.aws.resources.s3.s3_policy import S3Policy
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentityType
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy, InlinePolicy, ManagedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_base_iam_builder import CloudformationBaseIamBuilder
from cloudrail.knowledge.context.environment_context.common_component_builder import build_policy_statement
from cloudrail.knowledge.utils.arn_utils import build_arn

class CloudformationAssumeRolePolicyBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_ROLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> AssumeRolePolicy:
        res_properties: dict = cfn_res_attr['Properties']
        role_name: str = self._get_identity_name(cfn_res_attr, IamIdentityType.ROLE)
        qualified_arn: str = self._get_identity_arn(cfn_res_attr, IamIdentityType.ROLE)

        assume_role_statements: List[PolicyStatement] = []
        if assume_role_policy := self.get_property(res_properties, 'AssumeRolePolicyDocument'):
            assume_role_statements = [build_policy_statement(statement) for statement in assume_role_policy['Statement']]
        return AssumeRolePolicy(cfn_res_attr['account_id'],
                                role_name,
                                qualified_arn,
                                assume_role_statements,
                                assume_role_policy)


class CloudformationManagedPolicyBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_MANAGED_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> ManagedPolicy:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        policy_name = properties['ManagedPolicyName']
        arn = build_arn('iam', None, account, 'policy', self.get_property(properties, 'Path'), policy_name)
        policy: dict = self.get_property(properties, 'PolicyDocument', {})
        return ManagedPolicy(account=account,
                             policy_id=self.create_random_pseudo_identifier(),
                             policy_name=policy_name,
                             arn=arn,
                             statements=[build_policy_statement(statement) for statement in policy.get('Statement', [])],
                             raw_document=policy)


class CloudformationS3BucketPolicyBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.S3_BUCKET_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> S3Policy:
        properties: dict = cfn_res_attr['Properties']
        s3_policy: dict = self.get_property(properties, 'PolicyDocument')
        statements = [build_policy_statement(statement) for statement in s3_policy.get('Statement', [])] if s3_policy else []
        for statement in statements:
            for index, value in enumerate(statement.principal.principal_values):
                if value.isnumeric():
                    statement.principal.principal_values[index] = f'arn:aws:iam::{value}:root'
        return S3Policy(account=cfn_res_attr['account_id'],
                        bucket_name=self.get_property(properties, 'Bucket'),
                        statements=statements,
                        raw_document=s3_policy)


class CloudformationInlinePolicyFromRoleBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_ROLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[InlinePolicy]:
        res_properties: dict = cfn_res_attr['Properties']
        role_name: str = self._get_identity_name(cfn_res_attr, IamIdentityType.ROLE)
        return _build_inline_policy(cfn_res_attr['account_id'], res_properties, None, self.get_property, role_name)


class CloudformationInlinePolicyRoleBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Optional[List[InlinePolicy]]:
        properties: dict = cfn_res_attr['Properties']
        if 'Roles' in properties:
            return _build_inline_policy(cfn_res_attr['account_id'], properties, 'Roles', self.get_property)
        return None


class CloudformationInlinePolicyFromUserBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_USER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[InlinePolicy]:
        res_properties: dict = cfn_res_attr['Properties']
        user_name: str = self._get_identity_name(cfn_res_attr, IamIdentityType.USER)
        return _build_inline_policy(cfn_res_attr['account_id'], res_properties, None, self.get_property, user_name)


class CloudformationInlinePolicyUserBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Optional[List[InlinePolicy]]:
        properties: dict = cfn_res_attr['Properties']
        if 'Users' in properties:
            return _build_inline_policy(cfn_res_attr['account_id'], properties, 'Users', self.get_property)
        return None


class CloudformationInlinePolicyFromGroupBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[InlinePolicy]:
        res_properties: dict = cfn_res_attr['Properties']
        group_name: str = self._get_identity_name(cfn_res_attr, IamIdentityType.GROUP)
        return _build_inline_policy(cfn_res_attr['account_id'], res_properties, None, self.get_property, group_name)


class CloudformationInlinePolicyGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Optional[List[InlinePolicy]]:
        properties: dict = cfn_res_attr['Properties']
        if 'Groups' in properties:
            return _build_inline_policy(cfn_res_attr['account_id'], properties, 'Groups', self.get_property)
        return None


def _build_inline_policy(account:str, properties: dict, iam_string: Optional[str], get_property: Callable, owner_name: Optional[str] = None) -> List[InlinePolicy]:
    inline_policies: List[InlinePolicy] = []
    if not owner_name:
        policy_name = properties['PolicyName']
        policy: dict = get_property(properties, 'PolicyDocument', {})
        for identity in properties[iam_string]:
            inline_policies.append(InlinePolicy(account=account,
                                                owner_name=identity,
                                                policy_name=policy_name,
                                                statements=[build_policy_statement(statement) for statement in policy.get('Statement', [])],
                                                raw_document=policy))
    else:
        for inline_policy_dict in get_property(properties, 'Policies', []):
            policy: dict = get_property(inline_policy_dict, 'PolicyDocument', {})
            inline_policies.append(
                InlinePolicy(account=account,
                             owner_name=owner_name,
                             policy_name=get_property(inline_policy_dict, 'PolicyName'),
                             statements=[build_policy_statement(statement) for statement in policy.get('Statement', [])],
                             raw_document=policy))
    return inline_policies
