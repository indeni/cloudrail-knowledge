import unittest

from cloudrail.knowledge.context.aws.elb.load_balancer_listener import LoadBalancerListener
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_alb_is_using_https import EnsureLoadBalancerListenerIsUsingHttps
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureLoadBalancerListenerIsUsingHttps(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLoadBalancerListenerIsUsingHttps()

    def test_non_car_alb_https_fail(self):
        # Arrange
        lb_listener = LoadBalancerListener(listener_arn='listen_arn', listener_port=8080, listener_protocol='HTTP', load_balancer_arn='lb_arn',
                                           account='account', region='us-east-1', default_action_type='Direct', redirect_action_port='445',
                                           redirect_action_protocol='TCP')
        context = EnvironmentContext(load_balancer_listeners=[lb_listener])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is configured to use protocol HTTP on" in result.issues[0].evidence)

    def test_non_car_alb_https_redirect_fail(self):
        # Arrange
        lb_listener = LoadBalancerListener(listener_arn='listen_arn', listener_port=8080, listener_protocol='HTTP', load_balancer_arn='lb_arn',
                                           account='account', region='us-east-1', default_action_type='Redirect', redirect_action_port='445',
                                           redirect_action_protocol='HTTP')
        context = EnvironmentContext(load_balancer_listeners=[lb_listener])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is configured to redirect requests using HTTP protocol, and" in result.issues[0].evidence)

    def test_non_car_alb_https_pass(self):
        # Arrange
        lb_listener = LoadBalancerListener(listener_arn='listen_arn', listener_port=8080, listener_protocol='HTTP', load_balancer_arn='lb_arn',
                                           account='account', region='us-east-1', default_action_type='Redirect', redirect_action_port='445',
                                           redirect_action_protocol='HTTPS')
        context = EnvironmentContext(load_balancer_listeners=[lb_listener])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_alb_https_not_redirect_safe_proto_pass(self):
        # Arrange
        lb_listener = LoadBalancerListener(listener_arn='listen_arn', listener_port=8080, listener_protocol='HTTPS', load_balancer_arn='lb_arn',
                                           account='account', region='us-east-1', default_action_type='Direct', redirect_action_port='445',
                                           redirect_action_protocol='HTTPS')
        context = EnvironmentContext(load_balancer_listeners=[lb_listener])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
