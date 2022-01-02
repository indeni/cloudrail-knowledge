from abc import abstractmethod
from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AbstractPostgreSQLServersConfigurationEnabledRule(AzureBaseRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        pass

    @abstractmethod
    def get_configuration_name(self):
        pass

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for postgresql_servers in env_context.postgresql_servers:
            if postgresql_servers.postgresql_configuration:
                if postgresql_servers.postgresql_configuration.name == self.get_configuration_name() and\
                         not postgresql_servers.postgresql_configuration.value == 'on':
                    issues.append(
                        Issue(
                            f'The PostgreSQL Server `{postgresql_servers.get_friendly_name()}` does not have'
                            f' {self.get_configuration_name().replace("_", " ")} enabled.',
                            postgresql_servers, postgresql_servers))
        return issues


class PostgresqlServersHaveConnectionThrottlingEnabledRule(AbstractPostgreSQLServersConfigurationEnabledRule):
    def get_id(self) -> str:
        return 'non_car_postgresql_server_connection_throttling_enabled'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.postgresql_servers)

    @abstractmethod
    def get_configuration_name(self):
        return 'connection_throttling'


class PostgresqlServersHaveLogCheckpointsEnabledRule(AbstractPostgreSQLServersConfigurationEnabledRule):

    def get_id(self) -> str:
        return 'non_car_postgresql_server_log_checkpoints_enabled'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.postgresql_servers)

    def get_configuration_name(self):
        return 'log_checkpoints'


class PostgresqlServersHaveLogDisconnectionsEnabledRule(AbstractPostgreSQLServersConfigurationEnabledRule):

    def get_id(self) -> str:
        return 'non_car_postgresql_server_log_disconnections_enabled'

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.postgresql_servers)

    def get_configuration_name(self):
        return 'log_disconnections'
