from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_config_aggregator_enabled_all_regions_rule import \
    EnsureConfigAggregatorEnabledAllRegionsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureConfigAggregatorEnabledAllRegionsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureConfigAggregatorEnabledAllRegionsRule()

    @rule_test('account_all_regions_disabled', True)
    def test_account_all_regions_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('account_all_regions_enabled', False)
    def test_account_all_regions_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('organization_all_regions_disabled', True)
    def test_organization_all_regions_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('organization_all_regions_enabled', False)
    def test_organization_all_regions_enabled(self, rule_result: RuleResponse):
        pass
