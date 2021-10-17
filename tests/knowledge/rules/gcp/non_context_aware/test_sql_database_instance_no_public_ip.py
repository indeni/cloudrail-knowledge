from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.sql.gcp_sql_database_instance import GcpSqlDatabaseInstance, \
    GcpSqlDBInstanceSettings, GcpSqlDBInstanceSettingsIPConfig, GcpSqlDBInstanceIPConfigAuthNetworks
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_no_public_ip_rule import \
    SqlDatabaseNoPublicIpRule


class TestSqlDatabaseSslRequired(TestCase):
    def setUp(self):
        self.rule = SqlDatabaseNoPublicIpRule()

    @parameterized.expand(
        [
            ["have policy  ", True, True],
            ["no policy", False, False]
        ]
    )

    def test_cloud_sql_restrict_trusted_ip(self, unused_name: str, ipv4_enabled: bool, should_alert: bool):
        # Arrange
        sql = create_empty_entity(GcpSqlDatabaseInstance)
        sql.name = 'name'
        ip_configuration = GcpSqlDBInstanceSettingsIPConfig(authorized_networks=None,
                                                            ipv4_enabled=ipv4_enabled, private_network=None, require_ssl=None)
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