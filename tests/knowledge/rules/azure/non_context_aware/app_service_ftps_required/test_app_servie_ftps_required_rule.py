from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.app_service_ftps_required_rule import AppServiceFtpsRequiredRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestAppServiceFtpsRequiredRule(AzureBaseRuleTest):
    def get_rule(self):
        return AppServiceFtpsRequiredRule()

    @rule_test('ftps_only', should_alert=False)
    def test_ftps_only(self, rule_result: RuleResponse):
        pass

    @rule_test('no_site_config', should_alert=True)
    def test_no_site_config(self, rule_result: RuleResponse):
        pass

    @rule_test('all_allowed', should_alert=True)
    def test_all_allowed(self, rule_result: RuleResponse):
        pass

    @rule_test('disabled', should_alert=False)
    def test_disabled(self, rule_result: RuleResponse):
        pass
