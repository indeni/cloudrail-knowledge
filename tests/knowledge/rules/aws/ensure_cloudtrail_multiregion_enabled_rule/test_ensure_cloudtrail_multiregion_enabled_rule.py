from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_cloudtrail_multiregion_enabled_rule import EnsureCloudtrailMultiregionEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureCloudtrailMultiregionEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudtrailMultiregionEnabledRule()

    @rule_test('multiregion_disabled', True)
    def test_multiregion_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('multiregion_enabled', False)
    def test_multiregion_enabled(self, rule_result: RuleResponse):
        pass
