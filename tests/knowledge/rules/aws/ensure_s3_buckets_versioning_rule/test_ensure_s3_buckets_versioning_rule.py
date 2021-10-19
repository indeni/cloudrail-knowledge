from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_s3_buckets_versioning_rule import EnsureS3BucketsVersioningRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureS3BucketsVersioningRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketsVersioningRule()

    @rule_test('enabled', False)
    def test_versioning_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('disabled', True)
    def test_versioning_disabled(self, rule_result: RuleResponse):
        pass
