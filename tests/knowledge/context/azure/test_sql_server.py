from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSqlServer(AzureContextTest):

    def get_component(self):
        return "sql_server"

    @context(module_path="allow_public_access")
    def test_allow_public_access(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('test-sqlserver-cloudrail')
        self.assertIsNotNone(sql_server)
        self.assertTrue(sql_server.public_network_access_enable)
        if not sql_server.is_managed_by_iac:
            self.assertEqual(sql_server.get_cloud_resource_url(),
                             'https://portal.azure.com/#@871cad0f-903e-4648-9655-89b796e7c99e/resource/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/testresourcegroup/providers/Microsoft.Sql/servers/test-sqlserver-cloudrail/overview')

    @context(module_path="audit_enabled_extended_block")
    def test_audit_enabled_extended_block(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('cr2509-sqlserver')
        self.assertIsNotNone(sql_server)
        self.assertTrue(sql_server.extended_auditing_policy)
        self.assertTrue(sql_server.extended_auditing_policy.log_monitoring_enabled)
        self.assertEqual(sql_server.extended_auditing_policy.retention_in_days, 0)
        if sql_server.is_managed_by_iac:
            self.assertEqual(sql_server.extended_auditing_policy.server_id, 'azurerm_mssql_server.sql.id')
        else:
            self.assertEqual(sql_server.extended_auditing_policy.server_id, '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr2509-RG/providers/Microsoft.Sql/servers/cr2509-sqlserver')
            self.assertEqual(sql_server.extended_auditing_policy.get_cloud_resource_url(),
                             'https://portal.azure.com/#@871cad0f-903e-4648-9655-89b796e7c99e/resource/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr2509-RG/providers/Microsoft.Sql/servers/cr2509-sqlserver/serverAuditing')

    @context(module_path="audit_enabled_extended_block_default_retention")
    def test_audit_enabled_extended_block_default_retention(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('cr2509-sqlserver')
        self.assertIsNotNone(sql_server)
        self.assertTrue(sql_server.extended_auditing_policy)
        self.assertTrue(sql_server.extended_auditing_policy.log_monitoring_enabled)
        self.assertEqual(sql_server.extended_auditing_policy.retention_in_days, 0)
        self.assertTrue(sql_server.extended_auditing_policy.server_id)

    @context(module_path="audit_enabled_extended_block_retention_90")
    def test_audit_enabled_extended_block_retention_90(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('cr2509-sqlserver')
        self.assertIsNotNone(sql_server)
        self.assertTrue(sql_server.extended_auditing_policy)
        self.assertTrue(sql_server.extended_auditing_policy.log_monitoring_enabled)
        self.assertEqual(sql_server.extended_auditing_policy.retention_in_days, 90)
        self.assertTrue(sql_server.extended_auditing_policy.server_id)

    @context(module_path="audit_enabled_server_extended_resource_default_retention")
    def test_audit_enabled_server_extended_resource_default_retention(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('cr2509-sqlserver')
        self.assertIsNotNone(sql_server)
        self.assertTrue(sql_server.extended_auditing_policy)
        self.assertTrue(sql_server.extended_auditing_policy.log_monitoring_enabled)
        self.assertEqual(sql_server.extended_auditing_policy.retention_in_days, 0)
        self.assertTrue(sql_server.extended_auditing_policy.server_id)

    @context(module_path="audit_enabled_server_extended_resource_retention_90")
    def test_audit_enabled_server_extended_resource_retention_90(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('cr2509-sqlserver')
        self.assertIsNotNone(sql_server)
        self.assertTrue(sql_server.extended_auditing_policy)
        self.assertTrue(sql_server.extended_auditing_policy.log_monitoring_enabled)
        self.assertEqual(sql_server.extended_auditing_policy.retention_in_days,90)
        self.assertTrue(sql_server.extended_auditing_policy.server_id)

    @context(module_path="audit_not_enabled")
    def test_audit_not_enabled(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('cr2509-sqlserver')
        self.assertIsNotNone(sql_server)
        self.assertTrue(sql_server.extended_auditing_policy)
        self.assertFalse(sql_server.extended_auditing_policy.log_monitoring_enabled)
        self.assertEqual(sql_server.extended_auditing_policy.retention_in_days, 0)
        self.assertTrue(sql_server.extended_auditing_policy.server_id)
