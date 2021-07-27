from cloudrail.knowledge.context.azure.databases.azure_postgresql_server import AzurePostgreSqlServer
from cloudrail.knowledge.rules.azure.non_context_aware.postgresql_server_enforce_ssl_rule import PostgreSqlServerEnforceSslRule
from unittest import TestCase
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestPostgreSqlServerEnforceSslRule(TestCase):

    def setUp(self):
        self.rule = PostgreSqlServerEnforceSslRule()

    def test_non_car_postgresql_server_enforcing_ssl_fail(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        server.ssl_enforcement_enabled = False
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_postgresql_server_enforcing_ssl_pass(self):
        # Arrange
        server: AzurePostgreSqlServer = create_empty_entity(AzurePostgreSqlServer)
        server.ssl_enforcement_enabled = True
        context = AzureEnvironmentContext(postgresql_servers=AliasesDict(server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
