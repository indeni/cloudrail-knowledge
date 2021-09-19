from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_s3_bucket_logging_enabled_rule import \
    EnsureS3BucketLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureS3BucketLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketLoggingEnabledRule()

    def test_logging_disabled(self):
        self.run_test_case('logging_disabled', True, 2)

    def test_logging_enabled(self):
        self.run_test_case('logging_enabled', False)

    def test_logging_disabled_as_logger(self):
        self.run_test_case('logging_enabled_different_bucket', False)
