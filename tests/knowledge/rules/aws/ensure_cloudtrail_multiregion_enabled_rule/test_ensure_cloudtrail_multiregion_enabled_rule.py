from cloudrail.knowledge.rules.aws.non_context_aware.ensure_cloudtrail_multiregion_enabled_rule import EnsureCloudtrailMultiregionEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureCloudtrailMultiregionEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudtrailMultiregionEnabledRule()

    def test_multiregion_disabled(self):
        self.run_test_case('multiregion_disabled', True)

    def test_multiregion_enabled(self):
        self.run_test_case('multiregion_enabled', False)
