from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_alb_is_using_https import EnsureLoadBalancerListenerIsUsingHttps
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureLoadBalancerListenerIsUsingHttpsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureLoadBalancerListenerIsUsingHttps()

    def test_load_balancer_listener_http(self):
        rule_result = self.run_test_case('load_balancer_listener_http', True)
        self.assertEqual('aws_lb_listener.lb_listener_test',
                         rule_result.issues[0].exposed.iac_state.address)

    def test_load_balancer_listener_https(self):
        self.run_test_case('load_balancer_listener_https', False)

    def test_load_balancer_listener_http_redirect_https(self):
        self.run_test_case('load_balancer_listener_http_redirect_https', False)

    def test_load_balancer_listener_http_redirect_http(self):
        rule_result = self.run_test_case('load_balancer_listener_http_redirect_http', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is configured to redirect requests using HTTP protocol' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Load Balancer Listener')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Load Balancer Listener')

    def test_load_balancer_listener_http_redirect_http_url_port(self):
        rule_result = self.run_test_case('load_balancer_listener_http_redirect_http_url_port', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is configured to redirect requests using HTTP protocol' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Load Balancer Listener')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Load Balancer Listener')
