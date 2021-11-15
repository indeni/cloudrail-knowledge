import unittest
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance, GcpSqlDBInstanceSettings, \
    GcpSqlDBInstanceSettingsDBFlags, GcpSqlDBInstanceVersion
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_cross_databases_ownership_chaining_rule import SqlCrossDatabasesOwnershipChainingRule


class TestSqlDatabaseSslRequired(unittest.TestCase):

    def setUp(self):
        self.rule = SqlCrossDatabasesOwnershipChainingRule()

    @parameterized.expand([
            ["on", RuleResultType.FAILED, 1],
            ["off", RuleResultType.SUCCESS, 0]
        ])
    def test_sql_ownership_chaining(self, flag_mode: str, rule_status: RuleResultType, total_issues: int):
        # Arrange
        sql = create_empty_entity(GcpSqlDatabaseInstance)
        sql.name = 'name'
        sql.settings = create_empty_entity(GcpSqlDBInstanceSettings)
        sql.settings.database_flags = [GcpSqlDBInstanceSettingsDBFlags('cross db ownership chaining', flag_mode)]
        sql.database_version = GcpSqlDBInstanceVersion.SQLSERVER_2017_STANDARD
        context = GcpEnvironmentContext(sql_database_instances=[sql])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
