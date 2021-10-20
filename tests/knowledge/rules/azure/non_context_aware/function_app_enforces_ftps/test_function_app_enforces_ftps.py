from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_enforces_ftps_only_rule import FunctionAppEnforcesFtpsOnlyRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestFunctionAppEnforcesFtps(AzureBaseRuleTest):

    def get_rule(self):
        return FunctionAppEnforcesFtpsOnlyRule()

    @rule_test('ftps_enabled', should_alert=False)
    def test_ftps_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('ftps_disabled', should_alert=True)
    def test_ftps_disabled(self, rule_result: RuleResponse):
        pass
