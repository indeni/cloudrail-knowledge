from typing import Dict, List

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import \
    BypassTrafficType
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class StorageAccountAllowNetworkAccessTrustedAzureResourcesRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_storage_account_network_access_trusted_azure_services'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for storage_account in env_context.storage_accounts:
            if BypassTrafficType.AZURESERVICES not in storage_account.network_rules.bypass_traffic:
                issues.append(
                    Issue(
                        f'The {storage_account.get_type()} `{storage_account.get_friendly_name()}` is not allowing network access to trusted Azure services',
                        storage_account,
                        storage_account))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.storage_accounts)
