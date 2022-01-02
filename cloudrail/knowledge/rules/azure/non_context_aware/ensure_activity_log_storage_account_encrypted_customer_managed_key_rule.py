from typing import Dict, List

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureActivityLogStorageAccountEncryptedCustomerManagedKeyRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_activity_log_storage_account_encrypted_byok'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for monitor in env_context.monitor_diagnostic_settings:
            if storage_account := monitor.storage_account:
                if not storage_account.is_encrypted_by_customer_managed_key:
                    issues.append(
                        Issue(
                            f'The {storage_account.get_type()} `{storage_account.get_friendly_name()}` used for {monitor.get_friendly_name()} does not have BYOK encryption enabled',
                            storage_account,
                            storage_account))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.monitor_diagnostic_settings)
