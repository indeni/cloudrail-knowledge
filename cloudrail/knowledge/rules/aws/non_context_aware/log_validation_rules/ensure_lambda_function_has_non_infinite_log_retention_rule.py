from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureLambdaFunctionHasNonInfiniteLogRetentionRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_lambda_logging_not_infnite'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for lambda_func in env_context.lambda_function_list:
            if lambda_func.log_group.retention_in_days == 0 or not lambda_func.log_group.retention_in_days:
                if lambda_func.log_group.is_pseudo:
                    issues.append(
                        Issue(
                            f'Upon creation, {lambda_func.get_type()} `{lambda_func.get_friendly_name()}` '
                            f'will have a log group generated automatically with its retention set to Never Expire'
                            , lambda_func, lambda_func))
                else:
                    issues.append(
                        Issue(
                            f'The {lambda_func.log_group.get_type()} `{lambda_func.log_group.get_friendly_name()}` has '
                            f'retention set to Never Expire', lambda_func, lambda_func.log_group))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.lambda_function_list)
