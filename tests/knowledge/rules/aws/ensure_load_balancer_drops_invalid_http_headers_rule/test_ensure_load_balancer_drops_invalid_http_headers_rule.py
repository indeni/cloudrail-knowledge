from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_load_balancer_drops_invalid_http_headers_rule import \
    EnsureLoadBalancerDropsInvalidHttpHeadersRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureLoadBalancerDropsInvalidHttpHeadersRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLoadBalancerDropsInvalidHttpHeadersRule()

    @rule_test('invalid_headers_disabled', True)
    def test_invalid_headers_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('invalid_headers_enabled', False)
    def test_invalid_headers_enabled(self, rule_result: RuleResponse):
        pass
