from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_s3_bucket_policy_use_https_rule import EnsureS3BucketsPolicyUseHttpsRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureS3BucketsPolicyUseHttpsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketsPolicyUseHttpsRule()

    def test_secured_bucket(self):
        self.run_test_case('secured_bucket', False)

    def test_not_secured_bucket(self):
        self.run_test_case('not_secured_bucket', True)

    def test_no_policy(self):
        self.run_test_case('no_policy', True)
