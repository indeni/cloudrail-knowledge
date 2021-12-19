from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class KeyVaultDiagnosticLogsEnabledRule(AzureBaseRule):
    def get_id(self) -> str:
        return 'car_key_vault_diagnostic_logs_enabled'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for key_vault in env_context.key_vaults:
            key_vault_msg = f'Key Vault `{key_vault.server_name}`'
            if not key_vault.monitor_diagnostic_settings:
                issues.append(Issue(f'The {key_vault_msg} does not have diagnostic settings', key_vault, key_vault))
            else:
                for monitor_settings in key_vault.monitor_diagnostic_settings:

                    monitor_msg = f'The Monitor Diagnostic Setting {monitor_settings.server_name}, associated to {key_vault_msg},'
                    if not monitor_settings.logs_settings:
                        issues.append(Issue(f'{monitor_msg} does not have log block configuration', key_vault, key_vault))
                    elif not monitor_settings.logs_settings.enabled:
                        issues.append(Issue(f'{monitor_msg} does not have log enabled', key_vault, key_vault))
                    elif not monitor_settings.logs_settings.retention_policy:
                        issues.append(Issue(f'{monitor_msg} does not have a log retention policy', key_vault, key_vault))
                    elif not monitor_settings.logs_settings.retention_policy.enabled:
                        issues.append(Issue(f'{monitor_msg} have a disabled log retention policy', key_vault, key_vault))
                    elif 0 < monitor_settings.logs_settings.retention_policy.days < 365:
                        issues.append(Issue(f'{monitor_msg} does not have a log retention policy days equal to 0 or greater than or equal to 365',
                                            key_vault, key_vault))

        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.key_vaults)
