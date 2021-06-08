from datetime import datetime, timedelta
from typing import Dict, List, Optional

from cloudrail.knowledge.context.aws.iam.role import Role
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureUnusedRolesRemoved(BaseRule):

    def get_id(self) -> str:
        return 'non_car_unused_roles'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        effected_roles = self._get_unused_roles([role for role in env_context.roles if not role.is_new_resource()])
        for role in effected_roles:
            issues.append(
                Issue(
                    f'The {role.get_type()} `{role.get_friendly_name()}` has not been used for at least 90 days', role, role))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    # This rule depends on AWS account-data, in order to fetch info about last used date for IAM role.
    # Thus, adding "accounts" to the needed resources for this rule.
    # This rule will not run when running the evaluation with --no-cloud-account flag
    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.roles and environment_context.accounts)

    def _get_unused_roles(self, roles: List[Role]) -> List[Optional[Role]]:
        effected_roles_list = []
        current_date = datetime.today()
        for role in roles:
            if role.is_ever_used:
                self._get_affected_role(current_date, role.last_used_date.last_used_date, effected_roles_list, role)
            else:
                self._get_affected_role(current_date, role.creation_date, effected_roles_list, role)
        return effected_roles_list

    @staticmethod
    def _get_affected_role(current_date: datetime, date_string: str, roles_list: list, role: Role):
        subtract_date = datetime.strptime((date_string.split('T')[0]), '%Y-%m-%d')
        if current_date - subtract_date >= timedelta(days=90):
            roles_list.append(role)
