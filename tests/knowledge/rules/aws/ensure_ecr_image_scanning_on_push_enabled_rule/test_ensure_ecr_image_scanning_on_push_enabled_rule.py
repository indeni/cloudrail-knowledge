from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecr_image_scanning_on_push_enabled_rule import EnsureEcrImageScanningOnPushEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureEcrImageScanningOnPushEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcrImageScanningOnPushEnabledRule()

    @rule_test('image_scan_push_disabled', True)
    def test_image_scan_push_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('image_scan_push_enabled', False)
    def test_image_scan_push_enabled(self, rule_result: RuleResponse):
        pass
