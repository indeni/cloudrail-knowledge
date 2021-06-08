from typing import Dict, List

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IAMUserDirectlyAttachPoliciesRule(AwsBaseRule):

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues_list: List[Issue] = []
        for user in env_context.users:
            for policy in user.permissions_policies:
                issues_list.append(Issue(f"The user `{user.get_friendly_name()}` has the policy `{policy.get_friendly_name()}"
                                         f"`  attached directly to it",
                                         user, policy))
        return issues_list

    def get_id(self) -> str:
        return "non_car_iam_no_permissions_directly_to_user"

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.users)
