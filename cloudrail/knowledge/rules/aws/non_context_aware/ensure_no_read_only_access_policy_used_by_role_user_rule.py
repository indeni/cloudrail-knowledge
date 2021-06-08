from typing import Dict, List

from cloudrail.knowledge.context.aws.iam.iam_group import IamGroup
from cloudrail.knowledge.context.aws.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.aws.iam.role import Role
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_iam_readonlyaccess_policy'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        issue_items = self._get_iam_entities_issues(env_context.roles, env_context.users, env_context.users_login_profile)
        for item in issue_items:
            if isinstance(item, IamUser) and not self._is_read_only_policy(item):
                violating_groups: List[IamGroup] = [group for group in item.groups if self._is_read_only_policy(group)]
                issues.append(
                    Issue(
                        f'The {item.get_type()} `{item.get_friendly_name()}` inherit ReadOnlyAccess policy, '
                        f'via group(s) `{", ".join([group.get_friendly_name() for group in violating_groups])}` potentially'
                        f' risking contents in its AWS account',
                        violating_groups[0], violating_groups[0]))
            else:
                issues.append(
                    Issue(
                        f'The {item.get_type()} `{item.get_friendly_name()}` is assigned ReadOnlyAccess policy, '
                        f'potentially risking contents in its AWS account', item, item))
        return issues

    def _get_iam_entities_issues(self, roles: List[Role], users: List[IamUser], users_login_profile: List[IamUsersLoginProfile]) -> List[AwsResource]:
        users_login_list = [user_name.name for user_name in users_login_profile]
        issues_list = []
        for role in roles:
            if self._is_read_only_policy(role) and role.assume_role_policy.is_allowing_external_assume:
                if role not in issues_list:
                    issues_list.append(role)
        for user in users:
            if user.name in users_login_list:
                if self._is_user_or_group_has_read_only_policy(user):
                    if user not in issues_list:
                        issues_list.append(user)
        return issues_list

    @staticmethod
    def _is_read_only_policy(item: IamIdentity) -> bool:
        return any(policy.policy_name == 'ReadOnlyAccess' for policy in item.permissions_policies)

    def _is_user_or_group_has_read_only_policy(self, user: IamUser) -> bool:
        affected_groups = []
        for group in user.groups:
            if self._is_read_only_policy(group):
                affected_groups.append(group)
        return self._is_read_only_policy(user) or affected_groups

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.get_all_iam_entities())
