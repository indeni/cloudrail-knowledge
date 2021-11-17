from typing import Dict
from unittest import TestCase

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance, GcpSqlDBInstanceSettings, \
    GcpSqlDBInstanceSettingsDBFlags, GcpSqlDBInstanceVersion
from cloudrail.knowledge.rules.base_rule import RuleResultType, BaseRule
from cloudrail.knowledge.rules.gcp_rules_loader import GcpRulesLoader


class TestSqlDatabaseFlagsModes(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.rules_map: Dict[str, BaseRule] = GcpRulesLoader().load()

    @parameterized.expand([
            [
                'non_car_cloud_sql_contained_database_authentication_off', 'contained database authentication', 'on',
                GcpSqlDBInstanceVersion.SQLSERVER_2017_STANDARD, RuleResultType.FAILED, 1
            ],
            [
                'non_car_cloud_sql_contained_database_authentication_off', 'contained database authentication', 'on',
                GcpSqlDBInstanceVersion.POSTGRES10, RuleResultType.SUCCESS, 0
            ],
            [
                'non_car_cloud_sql_crossdb_ownership_chaining_on', 'cross db ownership chaining', 'on',
                GcpSqlDBInstanceVersion.SQLSERVER_2017_STANDARD, RuleResultType.FAILED, 1
            ],
            [
                'non_car_cloud_sql_crossdb_ownership_chaining_on', 'cross db ownership chaining', 'off',
                GcpSqlDBInstanceVersion.SQLSERVER_2017_STANDARD, RuleResultType.SUCCESS, 0
            ],
            [
                'non_car_cloud_sql_log_min_duration_disable', 'log_min_duration_statement', '0',
                GcpSqlDBInstanceVersion.POSTGRES10, RuleResultType.FAILED, 1
            ],
            [
                'non_car_cloud_sql_log_min_duration_disable', 'log_min_duration_statement', '-1',
                GcpSqlDBInstanceVersion.POSTGRES10, RuleResultType.SUCCESS, 0
            ],
            [
                'non_car_cloud_sql_log_temp_files_zero', 'log_temp_files', '1',
                GcpSqlDBInstanceVersion.POSTGRES10, RuleResultType.FAILED, 1
            ],
            [
                'non_car_cloud_sql_log_temp_files_zero', 'log_temp_files', '0',
                GcpSqlDBInstanceVersion.POSTGRES10, RuleResultType.SUCCESS, 0
            ],
            [
                'non_car_cloud_sql_log_lock_waits_on', 'log_lock_waits', 'off',
                GcpSqlDBInstanceVersion.POSTGRES11, RuleResultType.FAILED, 1
            ],
            [
                'non_car_cloud_sql_log_lock_waits_on', 'log_lock_waits', 'on',
                GcpSqlDBInstanceVersion.POSTGRES11, RuleResultType.SUCCESS, 0
            ],
            [
                'non_car_cloud_sql_log_disconnections_on', 'log_disconnections', 'on',
                GcpSqlDBInstanceVersion.POSTGRES11, RuleResultType.SUCCESS, 0
            ],
            [
                'non_car_cloud_sql_log_disconnections_on', 'log_disconnections', 'off',
                GcpSqlDBInstanceVersion.POSTGRES11, RuleResultType.FAILED, 1
            ],
            [
                'non_car_cloud_sql_log_connections_on', 'log_connections', 'on',
                GcpSqlDBInstanceVersion.POSTGRES11, RuleResultType.SUCCESS, 0
            ],
            [
                'non_car_cloud_sql_log_connections_on', 'log_connections', 'off',
                GcpSqlDBInstanceVersion.POSTGRES11, RuleResultType.FAILED, 1
            ],
            [
                'non_car_cloud_sql_log_checkpoints_on', 'log_checkpoints', 'on',
                GcpSqlDBInstanceVersion.POSTGRES11, RuleResultType.SUCCESS, 0
            ],
            [
                'non_car_cloud_sql_log_checkpoints_on', 'log_checkpoints', 'off',
                GcpSqlDBInstanceVersion.POSTGRES11, RuleResultType.FAILED, 1
            ]
        ])
    def test_sql_db_flag_mode(self, rule_id: str, flag_name: str, flag_value: str, db_version: GcpSqlDBInstanceVersion,
                              rule_status: RuleResultType, total_issues: int):
        # Arrange
        sql = create_empty_entity(GcpSqlDatabaseInstance)
        sql.name = 'name'
        sql.settings = create_empty_entity(GcpSqlDBInstanceSettings)
        sql.settings.database_flags = [GcpSqlDBInstanceSettingsDBFlags(flag_name, flag_value)]
        sql.database_version = db_version
        context = GcpEnvironmentContext(sql_database_instances=[sql])
        # Act
        result = self.rules_map.get(rule_id).run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
