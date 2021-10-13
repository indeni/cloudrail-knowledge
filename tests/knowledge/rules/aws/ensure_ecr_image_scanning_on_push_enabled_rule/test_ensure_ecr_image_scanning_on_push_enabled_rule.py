from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecr_image_scanning_on_push_enabled_rule import EnsureEcrImageScanningOnPushEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEcrImageScanningOnPushEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcrImageScanningOnPushEnabledRule()

    def test_image_scan_push_disabled(self):
        self.run_test_case('image_scan_push_disabled', True)

    def test_image_scan_push_enabled(self):
        self.run_test_case('image_scan_push_enabled', False)
