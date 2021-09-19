from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_cloudfront_protocol_version_is_good import\
    CloudFrontEnsureVersionRule


class TestCloudFrontEnsureVersionBaseRule(AwsBaseRuleTest):

    def get_rule(self):
        return CloudFrontEnsureVersionRule()

    def test_cloudfront_protocol_version_is_high(self):
        self.run_test_case('cloudfront_protocol_version_is_high', False)

    def test_cloudfront_protocol_version_is_low(self):
        self.run_test_case('cloudfront_protocol_version_is_low', True)

    def test_no_cloudfront_protocol_version_in_tf(self):
        self.run_test_case('no_cloudfront_protocol_version_in_tf', True)
