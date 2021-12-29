from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_security_alert_policy import AzureMsSqlServerSecurityAlertPolicyState
from cloudrail.knowledge.context.mergeable import EntityOrigin
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSqlServerSecurityAlertPolicy(AzureContextTest):

    def get_component(self):
        return "sql_server_security_alert_policy"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        alert_policy = next((policy for policy in ctx.sql_server_security_alert_policies
                                                 if policy.server_name == 'cr2523-sqlserver'), None)
        self.assertIsNotNone(alert_policy)
        self.assertEqual(alert_policy.email_addresses, [])
        self.assertEqual(alert_policy.disabled_alerts, [])
        self.assertFalse(alert_policy.email_account_admins)
        self.assertEqual(alert_policy.retention_days, 0)
        self.assertEqual(alert_policy.server_name, 'cr2523-sqlserver')
        self.assertEqual(alert_policy.state, AzureMsSqlServerSecurityAlertPolicyState.ENABLED)
        self.assertIsNone(alert_policy.storage_account_access_key)
        self.assertIsNone(alert_policy.storage_endpoint)
        self.assertTrue(alert_policy.vulnerability_assessment)
        self.assertIsNone(alert_policy.vulnerability_assessment.storage_container_sas_key)
        self.assertTrue(alert_policy.vulnerability_assessment.recurring_scans_settings)
        self.assertTrue(alert_policy.vulnerability_assessment.recurring_scans_settings.email_subscription_admins)
        self.assertTrue(alert_policy.vulnerability_assessment.recurring_scans_settings.enabled)
        self.assertEqual(alert_policy.vulnerability_assessment.recurring_scans_settings.emails, ['email@example1.com', 'email@example2.com'])
        if alert_policy.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(alert_policy.vulnerability_assessment.server_security_alert_policy_id,
                            '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr2523-RG/providers/Microsoft.Sql/servers/cr2523-sqlserver/securityAlertPolicies/Default')
            self.assertIsNone(alert_policy.vulnerability_assessment.storage_account_access_key)
            self.assertEqual(alert_policy.vulnerability_assessment.storage_container_path,
                             'https://cr2523tststoracc.blob.core.windows.net/cr2523container/')
        else:
            self.assertEqual(alert_policy.vulnerability_assessment.server_security_alert_policy_id, 'azurerm_mssql_server_security_alert_policy.example.id')
            self.assertEqual(alert_policy.vulnerability_assessment.storage_account_access_key, 'azurerm_storage_account.example.primary_access_key')
            self.assertEqual(alert_policy.vulnerability_assessment.storage_container_path, 'azurerm_storage_account.example.primary_blob_endpointcr2523container/')
