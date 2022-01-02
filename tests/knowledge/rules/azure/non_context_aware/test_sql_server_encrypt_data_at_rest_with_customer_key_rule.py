from unittest import TestCase
from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_transparent_data_encryption import AzureMsSqlServerTransparentDataEncryption
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.rules.azure.non_context_aware.sql_server_encrypt_data_at_rest_with_customer_key_rule import \
    SqlServerEncryptDataAtRestWithCustomerKeyRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestSqlServerEncryptDataAtRestWithCustomerKeyRule(TestCase):
    def setUp(self):
        self.rule = SqlServerEncryptDataAtRestWithCustomerKeyRule()

    @parameterized.expand(
        [
            ["no_encryption", False, True],
            ["encryption_enabled", True, False],
        ]
    )
    def test_sql_server_encrypt_data_at_rest_with_customer_key(self, unused_name: str, encrypting_enabled: bool, should_alert: bool):
        # Arrange
        sql_server: AzureSqlServer = create_empty_entity(AzureSqlServer)
        sql_server_transparent_data_encryption: AzureMsSqlServerTransparentDataEncryption = create_empty_entity(AzureMsSqlServerTransparentDataEncryption)
        sql_server_transparent_data_encryption.key_vault_key_id = 'some_key_id'
        if encrypting_enabled:
            sql_server.transparent_data_encryption = sql_server_transparent_data_encryption
        context = AzureEnvironmentContext(sql_servers=AliasesDict(sql_server),
                                          sql_server_transparent_data_encryptions=AliasesDict(sql_server_transparent_data_encryption))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
