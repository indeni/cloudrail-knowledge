from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_alb_is_using_https import EnsureLoadBalancerListenerIsUsingHttps
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureLoadBalancerListenerIsUsingHttpsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLoadBalancerListenerIsUsingHttps()

    @rule_test('load_balancer_listener_http', True)
    def test_load_balancer_listener_http(self, rule_result: RuleResponse):
        self.assertEqual('aws_lb_listener.lb_listener_test',
                         rule_result.issues[0].exposed.iac_state.address)

    @rule_test('load_balancer_listener_https', False)
    def test_load_balancer_listener_https(self, rule_result: RuleResponse):
        pass

    @rule_test('load_balancer_listener_http_redirect_https', False)
    def test_load_balancer_listener_http_redirect_https(self, rule_result: RuleResponse):
        pass

    @rule_test('load_balancer_listener_http_redirect_http', True)
    def test_load_balancer_listener_http_redirect_http(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is configured to redirect requests using HTTP protocol' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Load Balancer Listener')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Load Balancer Listener')

    @rule_test('load_balancer_listener_http_redirect_http_url_port', True)
    def test_load_balancer_listener_http_redirect_http_url_port(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('is configured to redirect requests using HTTP protocol' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Load Balancer Listener')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Load Balancer Listener')
