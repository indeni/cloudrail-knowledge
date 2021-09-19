from cloudrail.knowledge.rules.azure.non_context_aware.storage_account_allow_network_access_trusted_azure_services_rule import \
    StorageAccountAllowNetworkAccessTrustedAzureResourcesRule
from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestStorageAccountAllowNetworkAccessTrustedAzureResourcesRule(AzureBaseRuleTest):
    def get_rule(self):
        return StorageAccountAllowNetworkAccessTrustedAzureResourcesRule()

    def test_stacc_trusted_az_svc_allowed_by_default(self):
        self.run_test_case('stacc_trusted_az_svc_allowed_by_default', False)

    def test_stacc_trusted_az_svc_allowed_external_block(self):
        self.run_test_case('stacc_trusted_az_svc_allowed_external_block', False)

    def test_stacc_trusted_az_svc_allowed_internal_block(self):
        self.run_test_case('stacc_trusted_az_svc_allowed_internal_block', False)

    def test_stacc_trusted_az_svc_allowed_with_metrics(self):
        self.run_test_case('stacc_trusted_az_svc_allowed_with_metrics', False)

    def test_stacc_trusted_az_svc_not_allowed_external_block(self):
        self.run_test_case('stacc_trusted_az_svc_not_allowed_external_block', True)

    def test_stacc_trusted_az_svc_not_allowed_internal_block(self):
        self.run_test_case('stacc_trusted_az_svc_not_allowed_internal_block', True)
