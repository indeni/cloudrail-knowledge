from unittest import TestCase

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.rules.azure.non_context_aware.public_access_sql_database_rule import PublicAccessSqlDatabaseRule

from cloudrail.knowledge.rules.base_rule import RuleResultType

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestPublicAccessSqlDatabase(TestCase):

    def setUp(self):
        self.rule = PublicAccessSqlDatabaseRule()

    def test_public_access_enabled(self):
        # Arrange
        sql_server: AzureSqlServer = create_empty_entity(AzureSqlServer)
        sql_server.public_network_access_enable = True
        sql_server.server_name = 'my-sql-server'
        context = AzureEnvironmentContext(sql_servers=AliasesDict(sql_server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_disabled(self):
        # Arrange
        sql_server: AzureSqlServer = create_empty_entity(AzureSqlServer)
        sql_server.server_name = 'my-sql-server'
        context = AzureEnvironmentContext(sql_servers=AliasesDict(sql_server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
