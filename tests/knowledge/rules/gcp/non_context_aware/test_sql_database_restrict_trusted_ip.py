from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance, \
    GcpSqlDBInstanceSettings, GcpSqlDBInstanceSettingsIPConfig, GcpSqlDBInstanceIPConfigAuthNetworks
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_restrict_trusted_ip_rule import \
    SqlDatabaseRestrictTrustedIpRule


class TestSqlDatabaseSslRequired(TestCase):
    def setUp(self):
        self.rule = SqlDatabaseRestrictTrustedIpRule()

    @parameterized.expand(
        [
            [["8.8.4.0/24", "35.198.0.0/16", "107.178.192.0/18"], True, False],
            ["https_only disable", False, True]
        ]
    )

    def test_cloud_sql_restrict_trusted_ip(self, unused_name: str, config_auth_networks_value: list, should_alert: bool):
        # Arrange
        sql = create_empty_entity(GcpSqlDatabaseInstance)
        sql.name = 'name'
        authorized_networks = [GcpSqlDBInstanceIPConfigAuthNetworks(value="8.8.4.0/24", name=None, expiration_time=None)]
        ip_configuration = GcpSqlDBInstanceSettingsIPConfig(authorized_networks=authorized_networks)
        settings = GcpSqlDBInstanceSettings(ip_configuration=ip_configuration)
        sql.settings = settings
        context = GcpEnvironmentContext(sql_database_instances=[sql])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(should_alert, result.status)
