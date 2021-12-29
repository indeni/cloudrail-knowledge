from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.web_app_use_http_version_rule import AppServiceUseLatestHttpVersionRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServiceLatestHttpVersionRule(AzureBaseRuleTest):

    def get_rule(self):
        return AppServiceUseLatestHttpVersionRule()

    @rule_test('no_site_config', True)
    def test_app_service_no_site_config(self, rule_result: RuleResponse):
        pass

    @rule_test('http2_not_enabled', True)
    def test_app_service_http2_not_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('http2_enabled', False)
    def test_app_service_http2_enabled(self, rule_result: RuleResponse):
        pass
