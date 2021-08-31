from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PostgreSqlServerLogDisconnectionsEnabledRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_postgresql_server_log_disconnections_enabled'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for server in env_context.postgresql_servers:

            if not any([configuration for configuration in server.db_configurations
                        if configuration.name == 'log_disconnections' and configuration.value == 'on']):
                issues.append(
                    Issue(f'The {server.get_type()} `{server.get_friendly_name()}` does not have log disconnections enabled.',
                          server, server))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.postgresql_servers)
