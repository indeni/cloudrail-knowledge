from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_in_transit.ensure_cloudfront_distribution_encrypt_in_transit_rule \
    import \
    EnsureCloudfrontDistributionEncryptInTransitRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureCloudfrontDistributionEncryptInTransitRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureCloudfrontDistributionEncryptInTransitRule()

    @rule_test('not_encrypted', True)
    def test_not_encrypted(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("is not set to use HTTPS to protect data in transit default_cache_behavior and in"
                        " [\'ordered_cache_behavior #1\', \'ordered_cache_behavior #2\']" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'CloudFront Distribution')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_cloudfront_distribution.s3_distribution')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'CloudFront Distribution')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_cloudfront_distribution.s3_distribution')

    @rule_test('encrypted', False)
    def test_encrypted(self, rule_result: RuleResponse):
        pass
