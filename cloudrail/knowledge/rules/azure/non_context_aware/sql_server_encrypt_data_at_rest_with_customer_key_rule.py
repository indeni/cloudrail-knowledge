from typing import Dict, List

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class SqlServerEncryptDataAtRestWithCustomerKeyRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_sql_servers_encrypt_data_at_rest_customer_managed_keys'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for sql_server in env_context.sql_servers:
            if not sql_server.transparent_data_encryption or not sql_server.transparent_data_encryption.key_vault_key_id:
                issues.append(
                Issue(
                    f'The {sql_server.get_type()} `{sql_server.get_friendly_name()}` is not encrypting data at rest with a customer-managed key',
                    sql_server,
                    sql_server))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.sql_servers)
