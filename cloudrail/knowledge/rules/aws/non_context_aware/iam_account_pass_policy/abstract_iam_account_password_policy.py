from abc import abstractmethod
from typing import Callable, List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.iam.iam_password_policy import IamPasswordPolicy
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule

from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AbstractIamAccountPasswordPolicy(AwsBaseRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @staticmethod
    def _check_users(env_context: AwsEnvironmentContext) -> bool:
        users_login_list = [user_name.name for user_name in env_context.users_login_profile]
        return any(user.name in users_login_list for user in env_context.users)

    def _get_entities_list(self, env_context: AwsEnvironmentContext, policy_condition: Callable[[IamPasswordPolicy], bool]) \
            -> List[IamPasswordPolicy]:
        issues = []
        if self._check_users(env_context):
            for policy in env_context.iam_account_pass_policies:
                if policy_condition(policy):
                    issues.append(policy)
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.users
                    and environment_context.users_login_profile
                    and environment_context.iam_account_pass_policies)
