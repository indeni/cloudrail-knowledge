from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import BypassTrafficType, NetworkRuleDefaultAction
from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context


class TestStorageAccount(AzureContextTest):

    def get_component(self):
        return "storage_account"

    @context(module_path="default_network_access_allow_internal_block")
    def test_default_network_access_allow_internal_block(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2495tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.account_replication_type, 'LRS')
        self.assertEqual(storage_account.account_tier, 'Standard')
        self.assertTrue(storage_account.network_rules)
        self.assertEqual(storage_account.network_rules.default_action, NetworkRuleDefaultAction.ALLOW)
        self.assertEqual(storage_account.network_rules.ip_rules, [])
        if not storage_account.is_managed_by_iac:
            self.assertEqual(storage_account.get_cloud_resource_url(),
                             'https://portal.azure.com/#@871cad0f-903e-4648-9655-89b796e7c99e/resource/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr2495-RG/providers/Microsoft.Storage/storageAccounts/cr2495tststacc/overview')
            self.assertEqual(storage_account.network_rules.get_cloud_resource_url(),
                             'https://portal.azure.com/#@871cad0f-903e-4648-9655-89b796e7c99e/resource/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr2495-RG/providers/Microsoft.Storage/storageAccounts/cr2495tststacc/networking')

    @context(module_path="default_network_access_allow_no_block")
    def test_default_network_access_allow_no_block(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2495tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.account_replication_type, 'LRS')
        self.assertEqual(storage_account.account_tier, 'Standard')
        self.assertTrue(storage_account.network_rules)
        self.assertEqual(storage_account.network_rules.default_action, NetworkRuleDefaultAction.ALLOW)
        self.assertEqual(storage_account.network_rules.ip_rules, [])

    @context(module_path="default_network_access_deny_internal_block")
    def test_default_network_access_deny_internal_block(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2495tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.account_replication_type, 'LRS')
        self.assertEqual(storage_account.account_tier, 'Standard')
        self.assertTrue(storage_account.network_rules)
        self.assertEqual(storage_account.network_rules.default_action, NetworkRuleDefaultAction.DENY)
        self.assertEqual(storage_account.network_rules.ip_rules, ["134.5.8.1"])

    @context(module_path="storage_network_rules_allow")
    def test_storage_network_rules_allow(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2495tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.account_replication_type, 'LRS')
        self.assertEqual(storage_account.account_tier, 'Standard')
        self.assertTrue(storage_account.network_rules)
        self.assertEqual(storage_account.network_rules.default_action, NetworkRuleDefaultAction.ALLOW)
        self.assertEqual(storage_account.network_rules.ip_rules, ["1.2.3.4"])

    @context(module_path="storage_network_rules_deny")
    def test_storage_network_rules_deny(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2495tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.account_replication_type, 'LRS')
        self.assertEqual(storage_account.account_tier, 'Standard')
        self.assertTrue(storage_account.network_rules)
        self.assertEqual(storage_account.network_rules.default_action, NetworkRuleDefaultAction.DENY)
        self.assertEqual(storage_account.network_rules.ip_rules, ["1.2.3.4"])

    @context(module_path="stacc_trusted_az_svc_allowed_by_default")
    def test_stacc_trusted_az_svc_allowed_by_default(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2496tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.network_rules.bypass_traffic, [BypassTrafficType.AZURESERVICES])

    @context(module_path="stacc_trusted_az_svc_allowed_external_block")
    def test_stacc_trusted_az_svc_allowed_external_block(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2496tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.network_rules.bypass_traffic, [BypassTrafficType.AZURESERVICES])

    @context(module_path="stacc_trusted_az_svc_allowed_internal_block")
    def test_stacc_trusted_az_svc_allowed_internal_block(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2496tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.network_rules.bypass_traffic, [BypassTrafficType.AZURESERVICES])

    @context(module_path="stacc_trusted_az_svc_allowed_with_metrics")
    def test_stacc_trusted_az_svc_allowed_with_metrics(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2496tststacc')
        self.assertIsNotNone(storage_account)
        self.assertTrue(all(item in (BypassTrafficType.AZURESERVICES, BypassTrafficType.METRICS) for item in storage_account.network_rules.bypass_traffic))

    @context(module_path="stacc_trusted_az_svc_not_allowed_external_block")
    def test_stacc_trusted_az_svc_not_allowed_external_block(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2496tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.network_rules.bypass_traffic, [BypassTrafficType.METRICS])

    @context(module_path="stacc_trusted_az_svc_not_allowed_internal_block")
    def test_stacc_trusted_az_svc_not_allowed_internal_block(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2496tststacc')
        self.assertIsNotNone(storage_account)
        self.assertEqual(storage_account.network_rules.bypass_traffic, [BypassTrafficType.METRICS])

    @context(module_path="storage_account_secure_transfer_enabled")
    def test_storage_account_secure_transfer_enabled(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2494tststacc')
        self.assertIsNotNone(storage_account)
        self.assertTrue(storage_account.enable_https_traffic_only)

    @context(module_path="storage_account_secure_transfer_disabled")
    def test_storage_account_secure_transfer_disabled(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2494tststacc')
        self.assertIsNotNone(storage_account)
        self.assertFalse(storage_account.enable_https_traffic_only)

    @context(module_path="storage_account_public_access_enabled")
    def test_storage_account_public_access_enabled(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2493tststacc')
        self.assertIsNotNone(storage_account)
        self.assertTrue(storage_account.allow_blob_public_access)

    @context(module_path="storage_account_public_access_disabled")
    def test_storage_account_public_access_disabled(self, ctx: AzureEnvironmentContext):
        storage_account = ctx.storage_accounts.get('cr2493tststacc')
        self.assertIsNotNone(storage_account)
        self.assertFalse(storage_account.allow_blob_public_access)
