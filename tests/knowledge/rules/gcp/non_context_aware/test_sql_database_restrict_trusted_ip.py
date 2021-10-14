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
            ["cloud sql private ip", "8.8.4.0/24", "35.198.0.0/16", False],
            ["cloud sql private and open ip", "8.8.4.0/24", "0.0.0.0/0", True]
        ]
    )

    def test_cloud_sql_restrict_trusted_ip(self, unused_name: str, config_auth_networks_value_1: str,config_auth_networks_value_2: str, should_alert: bool):
        # Arrange
        sql = create_empty_entity(GcpSqlDatabaseInstance)
        sql.name = 'name'
        authorized_networks = [GcpSqlDBInstanceIPConfigAuthNetworks(value=config_auth_networks_value_1, name=None, expiration_time=None),
                               GcpSqlDBInstanceIPConfigAuthNetworks(value=config_auth_networks_value_2, name=None, expiration_time=None)]
        ip_configuration = GcpSqlDBInstanceSettingsIPConfig(authorized_networks=authorized_networks,
                                                            ipv4_enabled=None, private_network=None, require_ssl=None)
        settings = create_empty_entity(GcpSqlDBInstanceSettings)
        settings.ip_configuration = ip_configuration
        sql.settings = settings
        context = GcpEnvironmentContext(sql_database_instances=[sql])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
