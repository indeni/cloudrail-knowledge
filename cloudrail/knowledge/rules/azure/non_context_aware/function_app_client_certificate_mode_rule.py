from typing import List, Dict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.webapp.constants import FieldMode
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class FunctionAppClientCertificateModeRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_client_certificates_required_in_function_app'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for func_app in env_context.function_apps:
            if func_app.client_cert_mode != FieldMode.REQUIRED:
                issues.append(
                    Issue(
                        f'The Function App `{func_app.get_friendly_name()}` does not have client certificates mode set to required.',
                        func_app,
                        func_app))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)
