from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_s3_bucket_policy_use_https_rule import EnsureS3BucketsPolicyUseHttpsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureS3BucketsPolicyUseHttpsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureS3BucketsPolicyUseHttpsRule()

    @rule_test('secured_bucket', False)
    def test_secured_bucket(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secured_bucket', True)
    def test_not_secured_bucket(self, rule_result: RuleResponse):
        pass

    @rule_test('no_policy', True)
    def test_no_policy(self, rule_result: RuleResponse):
        pass
