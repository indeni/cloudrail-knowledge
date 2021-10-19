from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_use_latest_http_version_rule import FunctionAppUseLatestHttpVersionRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppUseLatestHttpVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUseLatestHttpVersionRule()

    @rule_test('function_app_no_site_config_block', True)
    def test_functionapp_no_site_config_block(self, rule_result: RuleResponse):
        pass

    @rule_test('functionapp_http2_not_enabled', True)
    def test_functionapp_http2_not_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('functionapp_http2_enabled', False)
    def test_functionapp_http2_enabled(self, rule_result: RuleResponse):
        pass
