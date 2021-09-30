from typing import List, Dict

from cloudrail.knowledge.context.aws.resources.s3.s3_policy import S3Policy
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy, InlinePolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_base_iam_builder import CloudformationBaseIamBuilder
from cloudrail.knowledge.context.environment_context.common_component_builder import build_policy_statement


class CloudformationAssumeRolePolicyBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_ROLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> AssumeRolePolicy:
        res_properties: dict = cfn_res_attr['Properties']
        role_name: str = self._get_role_name(cfn_res_attr)
        qualified_arn: str = self._get_role_arn(cfn_res_attr)

        assume_role_statements: List[PolicyStatement] = []
        if assume_role_policy := self.get_property(res_properties, 'AssumeRolePolicyDocument'):
            assume_role_statements = [build_policy_statement(statement) for statement in assume_role_policy['Statement']]
        return AssumeRolePolicy(cfn_res_attr['account_id'],
                                role_name,
                                qualified_arn,
                                assume_role_statements,
                                assume_role_policy)


class CloudformationInlineRolePolicyBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_ROLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[InlinePolicy]:
        res_properties: dict = cfn_res_attr['Properties']
        role_name: str = self._get_role_name(cfn_res_attr)
        inline_policies: List[InlinePolicy] = []

        for inline_policy_dict in self.get_property(res_properties, 'Policies', []):
            policy: dict = self.get_property(inline_policy_dict, 'PolicyDocument', {})
            inline_policies.append(
                InlinePolicy(account=cfn_res_attr['account_id'],
                             owner_name=role_name,
                             policy_name=self.get_property(inline_policy_dict, 'PolicyName'),
                             statements=[build_policy_statement(statement) for statement in policy.get('Statement', [])],
                             raw_document=policy))
        return inline_policies


class CloudformationS3BucketPolicyBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.S3_BUCKET_POLICY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> S3Policy:
        properties: dict = cfn_res_attr['Properties']
        s3_policy: dict = self.get_property(properties, 'PolicyDocument')
        return S3Policy(account=cfn_res_attr['account_id'],
                        bucket_name=self.get_property(properties, 'Bucket'),
                        statements=[build_policy_statement(statement) for statement in s3_policy.get('Statement', [])] if s3_policy else [],
                        raw_document=s3_policy)
