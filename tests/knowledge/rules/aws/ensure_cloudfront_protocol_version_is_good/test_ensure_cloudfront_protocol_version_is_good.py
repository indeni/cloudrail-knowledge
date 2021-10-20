from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_cloudfront_protocol_version_is_good import\
    CloudFrontEnsureVersionRule


class TestCloudFrontEnsureVersionBaseRule(AwsBaseRuleTest):

    def get_rule(self):
        return CloudFrontEnsureVersionRule()

    @rule_test('cloudfront_protocol_version_is_high', False)
    def test_cloudfront_protocol_version_is_high(self, rule_result: RuleResponse):
        pass

    @rule_test('cloudfront_protocol_version_is_low', True)
    def test_cloudfront_protocol_version_is_low(self, rule_result: RuleResponse):
        pass

    @rule_test('no_cloudfront_protocol_version_in_tf', True)
    def test_no_cloudfront_protocol_version_in_tf(self, rule_result: RuleResponse):
        pass
