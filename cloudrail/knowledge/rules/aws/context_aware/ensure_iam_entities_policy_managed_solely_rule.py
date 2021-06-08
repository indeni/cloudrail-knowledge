from typing import List, Dict, Tuple, Union

from cloudrail.knowledge.context.aws.account.account import Account
from cloudrail.knowledge.context.aws.iam.iam_group import IamGroup
from cloudrail.knowledge.context.aws.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.iam.policy import InlinePolicy, ManagedPolicy
from cloudrail.knowledge.context.mergeable import EntityOrigin
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureIamEntitiesPolicyManagedSolely(AwsBaseRule):

    def get_id(self) -> str:
        return 'car_iam_policy_control_in_iac_only'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for account in env_context.accounts:
            filtered_iam_entities = self._filter_entities_by_account(env_context.roles, account) + \
                                    self._filter_entities_by_account(env_context.users, account) + \
                                    self._filter_entities_by_account(env_context.groups, account)

            for entity in filtered_iam_entities:
                affected_policies = self._get_live_env_attached_policies(entity)
                for policy in affected_policies:
                    issues.append(
                        Issue(f'~`{policy.get_friendly_name()}`~. '
                              f'is attached to {entity.get_type()} `{entity.get_friendly_name()}`. `{entity.get_friendly_name()}` '
                              f'is declared in infrastructure-as-code. The attachment of the policy was done outside of the code '
                              f'(for example, directly via the console)', account, policy))
                if isinstance(entity, IamUser):
                    affected_groups = self._get_group_attach_policies_aws(entity)
                    for group, policies in affected_groups:
                        policies_list_string = ', '.join([policy.get_friendly_name() for policy in policies])
                        issues.append(
                            Issue(f'{entity.get_type()} `{entity.get_friendly_name()}` is declared in infrastructure-as-code. '
                                  f'The attachment of policy(s) `{policies_list_string}` to it was done outside the code '
                                  f'(for example, directly via the console), by adding it to the group `{group.get_friendly_name()}`.',
                                  account, group))
        return issues

    @staticmethod
    def filter_non_iac_managed_issues() -> bool:
        return False

    def _filter_entities_by_account(self, entities: List[IamIdentity], account: Account) -> List[IamIdentity]:
        return [entity for entity in entities if entity.account == account.account and self._are_there_existing_tf_entities(entity)]

    @staticmethod
    def _are_there_existing_tf_entities(entity: IamIdentity) -> bool:
        return entity.is_managed_by_iac and not entity.is_new_resource() and \
               any((isinstance(policy, ManagedPolicy) and
                    any(pao.get(policy.get_name()) == EntityOrigin.TERRAFORM for pao in entity.get_policies_attach_origin_maps())
                    or (isinstance(policy, InlinePolicy) and policy.is_managed_by_iac)) for policy in entity.get_policies())

    @staticmethod
    def _get_live_env_attached_policies(entity: IamIdentity) -> List[Union[ManagedPolicy, InlinePolicy]]:
        affected_policies = []
        for policy in entity.permissions_policies:
            if (isinstance(policy, ManagedPolicy)
                    and any(pao.get(policy.get_name()) == EntityOrigin.LIVE_ENV for pao in entity.get_policies_attach_origin_maps())):
                affected_policies.append(policy)
            elif isinstance(policy, InlinePolicy) and not policy.is_managed_by_iac:
                affected_policies.append(policy)
        return affected_policies

    def _get_group_attach_policies_aws(self, user: IamUser) -> List[Tuple[IamGroup, List[Union[ManagedPolicy, InlinePolicy]]]]:
        issues_list = []
        for group in user.groups:
            affected_policies = self._get_live_env_attached_policies(group)
            if affected_policies:
                issues_list.append((group, affected_policies))
        return issues_list

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.accounts and environment_context.get_all_iam_entities())
