from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import MsSqlServerMinimumTLSVersion, MsSqlServerVersion
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import ManagedIdentityType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_security_alert_policy import AzureMsSqlServerSecurityAlertPolicyState
from cloudrail.knowledge.context.mergeable import EntityOrigin
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSqlServer(AzureContextTest):

    def get_component(self):
        return "sql_server"

    @context(module_path="allow_public_access")
    def test_allow_public_access(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('test-sqlserver-cloudrail')
        self.assertIsNotNone(sql_server)
        self.assertTrue(sql_server.public_network_access_enabled)
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

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        sql_server = ctx.sql_servers.get('cr2523-sqlserver')
        self.assertIsNotNone(sql_server)
        self.assertEqual(sql_server.administrator_login, '4dm1n157r470r')
        self.assertEqual(sql_server.minimum_tls_version, MsSqlServerMinimumTLSVersion.VERSION_1_1)
        self.assertFalse(sql_server.public_network_access_enabled)
        self.assertEqual(sql_server.tags, {'environment': 'production'})
        self.assertEqual(sql_server.version, MsSqlServerVersion.VERSION_12_0)
        self.assertEqual(len(sql_server.azuread_administrator_list), 1)
        self.assertEqual(sql_server.azuread_administrator_list[0].login_username, 'sqladmin')
        self.assertEqual(sql_server.azuread_administrator_list[0].object_id, 'ddc8b952-aa8e-4ae1-aa42-0dfdf4f15db3')
        self.assertEqual(sql_server.azuread_administrator_list[0].tenant_id, '568db8f3-e402-4c09-baa9-692e42029cc7')
        self.assertFalse(sql_server.azuread_administrator_list[0].azuread_authentication_only)
        self.assertEqual(len(sql_server.managed_identities), 1)
        self.assertEqual(sql_server.managed_identities[0].identity_name, 'cr2523-userid')
        self.assertEqual(sql_server.managed_identities[0].identity_type, ManagedIdentityType.USER_ASSIGNED)
        for alert_policy in sql_server.security_alert_policy_list:
            self.assertEqual(alert_policy.email_addresses, [])
            self.assertEqual(alert_policy.disabled_alerts, [])
            self.assertFalse(alert_policy.email_account_admins)
            self.assertEqual(alert_policy.retention_days, 0)
            self.assertEqual(alert_policy.server_name, 'cr2523-sqlserver')
            self.assertEqual(alert_policy.state, AzureMsSqlServerSecurityAlertPolicyState.ENABLED)
            self.assertIsNone(alert_policy.storage_account_access_key)
            self.assertIsNone(alert_policy.storage_endpoint)
        self.assertTrue(sql_server.transparent_data_encryption)
        if sql_server.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(sql_server.primary_user_assigned_identity_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourcegroups/cr2523-RG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/cr2523-userid')
            self.assertEqual(sql_server.transparent_data_encryption.server_id, 'cr2523-sqlserver')
            self.assertEqual(sql_server.transparent_data_encryption.key_vault_key_id,
                             'https://cr2523-keyvault.vault.azure.net/keys/cr2523-sqlkey/102c284260c94b2290745bb3487fa40b')
            self.assertEqual(sql_server.user_assigned_identity_ids,
                             ['/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourcegroups/cr2523-RG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/cr2523-userid'])
        else:
            self.assertEqual(sql_server.primary_user_assigned_identity_id, 'azurerm_user_assigned_identity.sql.id')
            self.assertEqual(sql_server.transparent_data_encryption.server_id, 'azurerm_mssql_server.sql.id')
            self.assertEqual(sql_server.transparent_data_encryption.key_vault_key_id,
                             'azurerm_key_vault_key.key.id')
