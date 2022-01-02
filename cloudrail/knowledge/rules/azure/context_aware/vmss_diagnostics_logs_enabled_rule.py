from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class VmssDiagnosticsLogsEnabledRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'car_virtual_machine_scale_set_diagnostic_logs_enabled'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for vmss in env_context.virtual_machines_scale_sets:
            if not vmss.is_diagnostics_logs_enabled:
                issues.append(
                    Issue(
                        f'The {vmss.get_type()} `{vmss.get_friendly_name()}` does not have diagnostic settings enabled.',
                        vmss,
                        vmss))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.virtual_machines_scale_sets)
