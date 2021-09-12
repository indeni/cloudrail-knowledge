from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import NetworkRuleDefaultAction
from typing import List, Dict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureStorageAccountDefaultNetworkDenyRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_storage_account_default_network_access_denied'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for storage in env_context.storage_accounts:
            if storage.network_rules.default_action == NetworkRuleDefaultAction.ALLOW:
                issues.append(
                    Issue(
                        f'The {storage.get_type()} `{storage.get_friendly_name()}` is not denying default network access',
                        storage,
                        storage))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.storage_accounts)
