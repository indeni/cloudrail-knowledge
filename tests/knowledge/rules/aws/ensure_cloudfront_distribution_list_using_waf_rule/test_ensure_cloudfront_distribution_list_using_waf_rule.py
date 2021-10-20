from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_cloudfront_distribution_list_using_waf_rule import \
    CloudFrontEnsureWafUsedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestCloudFrontEnsureWafUsedRule(AwsBaseRuleTest):

    def get_rule(self):
        return CloudFrontEnsureWafUsedRule()

    @rule_test('waf_disabled', True)
    def test_waf_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('waf_enabled', False)
    def test_waf_enabled(self, rule_result: RuleResponse):
        pass
