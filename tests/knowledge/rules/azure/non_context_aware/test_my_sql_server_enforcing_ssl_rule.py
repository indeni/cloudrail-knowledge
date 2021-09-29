from cloudrail.knowledge.context.azure.resources.databases.azure_mysql_server import AzureMySqlServer
from cloudrail.knowledge.rules.azure.non_context_aware.my_sql_server_enforcing_ssl_rule import MySqlServerEnforcingSslRule
from unittest import TestCase
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestMySqlServerEnforcingSslRule(TestCase):

    def setUp(self):
        self.rule = MySqlServerEnforcingSslRule()

    def test_non_car_mysql_server_enforcing_ssl_fail(self):
        # Arrange
        my_sql_server: AzureMySqlServer = create_empty_entity(AzureMySqlServer)
        my_sql_server.ssl_enforcement_enabled = False
        context = AzureEnvironmentContext(my_sql_servers=AliasesDict(my_sql_server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_mysql_server_enforcing_ssl_pass(self):
        # Arrange
        my_sql_server: AzureMySqlServer = create_empty_entity(AzureMySqlServer)
        my_sql_server.ssl_enforcement_enabled = True
        context = AzureEnvironmentContext(my_sql_servers=AliasesDict(my_sql_server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
