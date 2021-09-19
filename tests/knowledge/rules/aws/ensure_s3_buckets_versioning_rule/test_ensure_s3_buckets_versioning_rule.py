from cloudrail.knowledge.rules.aws.non_context_aware.ensure_s3_buckets_versioning_rule import EnsureS3BucketsVersioningRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureS3BucketsVersioningRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketsVersioningRule()

    def test_versioning_enabled(self):
        self.run_test_case('enabled', False)

    def test_versioning_disabled(self):
        self.run_test_case('disabled', True)
