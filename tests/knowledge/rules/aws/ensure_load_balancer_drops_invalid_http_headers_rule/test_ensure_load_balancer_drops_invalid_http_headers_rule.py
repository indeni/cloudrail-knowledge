from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_load_balancer_drops_invalid_http_headers_rule import \
    EnsureLoadBalancerDropsInvalidHttpHeadersRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureLoadBalancerDropsInvalidHttpHeadersRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLoadBalancerDropsInvalidHttpHeadersRule()

    def test_invalid_headers_disabled(self):
        self.run_test_case('invalid_headers_disabled', True)

    def test_invalid_headers_enabled(self):
        self.run_test_case('invalid_headers_enabled', False)
