from cloudrail.knowledge.rules.azure.non_context_aware.app_service_use_latest_tls_version_rule import AppServiceUseLatestTlsVersionRule

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestAppServiceUseLatestTlsVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceUseLatestTlsVersionRule()

    def test_tls_1_1(self):
        self.run_test_case('webapp_tls_1_1', should_alert=True)

    def test_tls_1_2(self):
        self.run_test_case('webapp_tls_1_2', should_alert=False)

    def test_tls_missing(self):
        self.run_test_case('webapp_tls_missing', should_alert=False)
