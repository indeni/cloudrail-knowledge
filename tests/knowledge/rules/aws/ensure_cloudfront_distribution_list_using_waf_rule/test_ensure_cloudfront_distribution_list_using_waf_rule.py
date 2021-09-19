from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_cloudfront_distribution_list_using_waf_rule import \
    CloudFrontEnsureWafUsedRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestCloudFrontEnsureWafUsedRule(AwsBaseRuleTest):

    def get_rule(self):
        return CloudFrontEnsureWafUsedRule()

    def test_waf_disabled(self):
        self.run_test_case('waf_disabled', True)

    def test_waf_enabled(self):
        self.run_test_case('waf_enabled', False)
