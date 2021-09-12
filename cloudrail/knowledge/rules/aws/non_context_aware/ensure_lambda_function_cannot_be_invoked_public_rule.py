from typing import List, Dict, Optional
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.action_utils import get_intersected_actions


class EnsureLambdaFunctionCannotBeInvokedPublicRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_lambda_public_exposure'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for lambda_func in env_context.lambda_function_list:
            if self._is_lambda_can_publicly_invoked(lambda_func.resource_based_policy):
                issues.append(
                    Issue(
                        f'The {lambda_func.get_type()} `{lambda_func.get_friendly_name()}` is exposed because its resource policy is too permissive.',
                        lambda_func, lambda_func))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.lambda_function_list)

    @staticmethod
    def _is_lambda_can_publicly_invoked(lambda_policy: Optional[Policy]) -> bool:
        if not lambda_policy:
            return False
        return any(statement.effect == StatementEffect.ALLOW
                   and not statement.condition_block
                   and get_intersected_actions(statement.actions, 'lambda:InvokeFunction')
                   and ((any(value in ('*', '*.amazonaws.com') for value in statement.principal.principal_values)
                         or not statement.principal.principal_values))
                   for statement in lambda_policy.statements)
