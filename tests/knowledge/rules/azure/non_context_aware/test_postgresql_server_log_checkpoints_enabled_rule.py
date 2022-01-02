from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server import AzurePostgreSqlServer
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server_configuration import \
    AzurePostgreSqlServerConfiguration
from cloudrail.knowledge.rules.azure.non_context_aware.abstract_postgresql_servers_have_configuration_value_enabled_rule import \
    PostgresqlServersHaveLogCheckpointsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestPostgresqlServersHaveLogCheckpointsEnabledRule(TestCase):

    def setUp(self):
        self.rule = PostgresqlServersHaveLogCheckpointsEnabledRule()

    @parameterized.expand(
        [
            ["log_checkpoints enabled", 'log_checkpoints', 'on', False],
            ["log_checkpoints disable", 'log_checkpoints', 'off', True],
            ["not log_checkpoints", '', 'off', False]
        ]
    )
    def test_auth_states(self, unused_name: str, name: str, value: str, should_alert: bool):
        # Arrange
        postgresql_servers: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        postgresql_configuration = create_empty_entity(AzurePostgreSqlServerConfiguration)
        postgresql_configuration.value = value
        postgresql_configuration.name = name
        postgresql_servers.postgresql_configuration = postgresql_configuration
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(postgresql_servers))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
