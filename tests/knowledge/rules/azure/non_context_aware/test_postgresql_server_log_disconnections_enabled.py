from unittest import TestCase
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.databases.azure_database_configuration import AzureDatabaseConfiguration
from cloudrail.knowledge.context.azure.resources.databases.azure_postgresql_server import AzurePostgreSqlServer
from cloudrail.knowledge.rules.azure.non_context_aware.postgresql_server_log_disconnections_enabled_rule import \
    PostgreSqlServerLogDisconnectionsEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestPostgreSqlServerLogDisconnectionsEnabled(TestCase):

    def setUp(self):
        self.rule = PostgreSqlServerLogDisconnectionsEnabledRule()

    def test_non_car_postgresql_server_log_disconnections_enabled_passed(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        server.db_configurations = [AzureDatabaseConfiguration('log_disconnections', 'on', 'psqlServer')]
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_postgresql_server_log_disconnections_disabled_failed(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        server.db_configurations = [AzureDatabaseConfiguration('log_disconnections', 'off', 'psqlServer')]
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue(isinstance(result.issues[0].violating, AzureDatabaseConfiguration))

    def test_non_car_postgresql_server_db_config_missing_failed(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        # server.db_configurations = [AzureDatabaseConfiguration('log_disconnections', 'off', 'psqlServer')] -- leave it in a comment
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue(isinstance(result.issues[0].violating, AzurePostgreSqlServer))

    def test_non_car_postgresql_server_log_disconnections_not_exist_failed(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        server.db_configurations = [AzureDatabaseConfiguration('some_conf', 'off', 'psqlServer')]
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue(isinstance(result.issues[0].violating, AzurePostgreSqlServer))

    def test_non_car_postgresql_server_log_disconnections_enabled_multi_value_passed(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        server.db_configurations = [AzureDatabaseConfiguration('log_disconnections', 'on', 'psqlServer'),
                                    AzureDatabaseConfiguration('backslash_quote', 'on', 'psqlServer')]
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_postgresql_server_log_disconnections_disabled_multi_value_failed(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        server.db_configurations = [AzureDatabaseConfiguration('log_disconnections', 'off', 'psqlServer'),
                                    AzureDatabaseConfiguration('backslash_quote', 'on', 'psqlServer')]
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue(isinstance(result.issues[0].violating, AzureDatabaseConfiguration))

    def test_non_car_postgresql_server_log_disconnections_missing_multi_value_failed(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        server.db_configurations = [AzureDatabaseConfiguration('some_conf', 'off', 'psqlServer'),
                                    AzureDatabaseConfiguration('backslash_quote', 'on', 'psqlServer')]
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue(isinstance(result.issues[0].violating, AzurePostgreSqlServer))
