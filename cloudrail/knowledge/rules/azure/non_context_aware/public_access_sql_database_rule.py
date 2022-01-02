from typing import Dict, List

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PublicAccessSqlDatabaseRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_azure_database_public_access'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for sql_server in env_context.sql_servers:
            if sql_server.public_network_access_enabled:
                issues.append(
                    Issue(
                        f'~{sql_server.get_type()}~. '
                        f'{sql_server.get_type()} with database name `{sql_server.get_friendly_name()}` is exposed to the internet',
                        sql_server,
                        sql_server))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.sql_servers)
