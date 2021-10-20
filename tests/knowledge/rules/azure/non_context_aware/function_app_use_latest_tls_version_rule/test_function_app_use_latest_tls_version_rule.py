from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_use_latest_tls_version_rule import FunctionAppUseLatestTlsVersionRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppUseLatestTlsVersionRule(AzureBaseRuleTest):
    def get_rule(self):
        return FunctionAppUseLatestTlsVersionRule()

    @rule_test('functionapp_tls_isnot_latest', True)
    def test_functionapp_tls_isnot_latest(self, rule_result: RuleResponse):
        pass

    @rule_test('functionapp_tls_latest', False)
    def test_functionapp_tls_latest(self, rule_result: RuleResponse):
        pass
