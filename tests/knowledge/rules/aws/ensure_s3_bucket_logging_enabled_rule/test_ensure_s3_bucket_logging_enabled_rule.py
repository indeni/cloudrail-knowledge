from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_s3_bucket_logging_enabled_rule import \
    EnsureS3BucketLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureS3BucketLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketLoggingEnabledRule()

    @rule_test('logging_disabled', True, 2)
    def test_logging_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('logging_enabled', False)
    def test_logging_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('logging_enabled_different_bucket', False)
    def test_logging_disabled_as_logger(self, rule_result: RuleResponse):
        pass
