from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudtrail_log_validation_enabled_rule import \
    EnsureCloudTrailLogValidationEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest

class TestEnsureCloudTrailLogValidationEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudTrailLogValidationEnabledRule()

    def test_file_log_validation_disabled(self):
        self.run_test_case('file_log_validation_disabled', True)

    def test_file_log_validation_enabled(self):
        self.run_test_case('file_log_validation_enabled', False)
