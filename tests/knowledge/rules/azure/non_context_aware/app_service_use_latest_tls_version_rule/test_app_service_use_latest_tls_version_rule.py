from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_use_latest_tls_version_rule import AppServiceUseLatestTlsVersionRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServiceUseLatestTlsVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceUseLatestTlsVersionRule()

    @rule_test('webapp_tls_1_1', should_alert=True)
    def test_tls_1_1(self, rule_result: RuleResponse):
        pass

    @rule_test('webapp_tls_1_2', should_alert=False)
    def test_tls_1_2(self, rule_result: RuleResponse):
        pass

    @rule_test('webapp_tls_missing', should_alert=False)
    def test_tls_missing(self, rule_result: RuleResponse):
        pass
