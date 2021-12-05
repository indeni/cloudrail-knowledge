from typing import List, Dict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class FunctionAppUseManagedIdentityRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_function_app_using_managed_identity'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for func_app in env_context.function_apps:
            if func_app.identity is None or func_app.identity.type not in ['SystemAssigned', 'UserAssigned']:
                issues.append(
                    Issue(
                        f'The {func_app.get_type()} `{func_app.get_friendly_name()}` '
                        f'does not have managed identity enabled.', func_app, func_app))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)
