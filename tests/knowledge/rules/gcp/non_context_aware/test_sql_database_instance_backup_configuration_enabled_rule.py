from typing import List
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance, \
    GcpSqlDBInstanceSettings, GcpSqlDBInstanceSettingsBackupConfig
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_backup_configuration_enabled_rule import SqlDatabaseBackupConfigurationEnabledRule


class TestSqlDatabaseBackupConfigurationEnabledRule(TestCase):
    def setUp(self):
        self.rule = SqlDatabaseBackupConfigurationEnabledRule()

    @parameterized.expand(
        [
            ["Two cloud SQL database instances backup configuration enabled", [True, True], 0, False],
            ["One cloud SQL database instances backup configuration enabled", [True, False], 1, True],
            ["No cloud SQL database instances backup configuration enabled", [False, False], 2, True],
        ]
    )

    def test_cloud_sql_backup_configuration_enabled(self, unused_name: str, enables: List[bool], issuses: int, should_alert: bool):
        # Arrange
        sqls = []
        for i, enabled in enumerate(enables, 1):
            sql = create_empty_entity(GcpSqlDatabaseInstance)
            sql.name = 'name_' + str(i)
            sql.settings = create_empty_entity(GcpSqlDBInstanceSettings)
            sql.settings.backup_configuration = create_empty_entity(GcpSqlDBInstanceSettingsBackupConfig)
            sql.settings.backup_configuration.enabled = enabled
            sqls.append(sql)

        context = GcpEnvironmentContext(sql_database_instances=[*sqls])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(issuses, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
