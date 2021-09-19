from cloudrail.knowledge.rules.aws.non_context_aware.ensure_config_aggregator_enabled_all_regions_rule import \
    EnsureConfigAggregatorEnabledAllRegionsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureConfigAggregatorEnabledAllRegionsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureConfigAggregatorEnabledAllRegionsRule()

    def test_account_all_regions_disabled(self):
        self.run_test_case('account_all_regions_disabled', True)

    def test_account_all_regions_enabled(self):
        self.run_test_case('account_all_regions_enabled', False)

    def test_organization_all_regions_disabled(self):
        self.run_test_case('organization_all_regions_disabled', True)

    def test_organization_all_regions_enabled(self):
        self.run_test_case('organization_all_regions_enabled', False)
