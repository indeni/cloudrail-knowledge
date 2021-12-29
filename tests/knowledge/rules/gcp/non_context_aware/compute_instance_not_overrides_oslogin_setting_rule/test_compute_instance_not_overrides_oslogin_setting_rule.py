from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_not_overrides_oslogin_setting_rule import ComputeInstanceNotOverridesOsLoginSettingRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeInstanceNotOverridesOsLoginSettingRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeInstanceNotOverridesOsLoginSettingRule()

    @rule_test('both_enable_oslogin_true', should_alert=False,)
    def test_both_enable_oslogin_true(self, rule_result: RuleResponse):
        pass

    @rule_test('one_enable_oslogin_true_second_false', should_alert=True)
    def test_one_enable_oslogin_true_second_false(self, rule_result: RuleResponse):
        pass

    @rule_test('without_enable_oslogin', should_alert=False)
    def test_without_enable_oslogin(self, rule_result: RuleResponse):
        pass
