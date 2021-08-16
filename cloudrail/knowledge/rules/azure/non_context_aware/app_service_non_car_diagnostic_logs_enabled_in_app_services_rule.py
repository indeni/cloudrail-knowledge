from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AppServiceDiagnosticLogsRule(AzureBaseRule):
    def get_id(self) -> str:
        return 'non_car_diagnostic_logs_enabled_in_app_services'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for app_service in env_context.app_services:

            if app_service.app_service_config is not None:
                app_service_name = app_service.get_friendly_name()
                if app_service.app_service_config.logs is None:
                    issues.append(
                        Issue(f'The web app `{app_service_name}` does not have logging enabled', app_service, app_service))
                else:
                    evidence: List[str] = []
                    if not app_service.app_service_config.logs.http_logging_enabled:
                        evidence.append(
                            f'The web app `{app_service_name}` does not have HTTP logging enabled')
                    if not app_service.app_service_config.logs.request_tracing_enabled:
                        evidence.append(
                            f'The web app `{app_service_name}` does not have request tracing enabled')
                    if not app_service.app_service_config.logs.detailed_error_logging_enabled:
                        evidence.append(
                            f'The web app `{app_service_name}` does not have detailed error logging enabled')
                    if evidence:
                        issues.append(
                            Issue('. '.join(evidence), app_service, app_service))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.app_services)
