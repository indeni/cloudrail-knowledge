import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer, LoadBalancerType
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_attributes import LoadBalancerAttributes
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_load_balancer_drops_invalid_http_headers_rule import \
    EnsureLoadBalancerDropsInvalidHttpHeadersRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureLoadBalancerDropsInvalidHttpHeadersRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLoadBalancerDropsInvalidHttpHeadersRule()

    def test_non_car_alb_drops_invalid_http_headers_fail(self):
        # Arrange
        load_balancer: LoadBalancer = create_empty_entity(LoadBalancer)
        lb_attributes: LoadBalancerAttributes = create_empty_entity(LoadBalancerAttributes)
        lb_attributes.drop_invalid_header_fields = False
        load_balancer.load_balancer_type = LoadBalancerType.APPLICATION
        load_balancer.load_balancer_attributes = lb_attributes
        context = AwsEnvironmentContext(load_balancers=[load_balancer])

        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_alb_drops_invalid_http_headers_pass(self):
        # Arrange
        load_balancer: LoadBalancer = create_empty_entity(LoadBalancer)
        lb_attributes: LoadBalancerAttributes = create_empty_entity(LoadBalancerAttributes)
        lb_attributes.drop_invalid_header_fields = True
        load_balancer.load_balancer_type = LoadBalancerType.APPLICATION
        load_balancer.load_balancer_attributes = lb_attributes
        context = AwsEnvironmentContext(load_balancers=[load_balancer])

        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_alb_drops_invalid_http_headers__network_lb__pass(self):
        # Arrange
        load_balancer: LoadBalancer = create_empty_entity(LoadBalancer)
        lb_attributes: LoadBalancerAttributes = create_empty_entity(LoadBalancerAttributes)
        lb_attributes.drop_invalid_header_fields = True
        load_balancer.load_balancer_type = LoadBalancerType.NETWORK
        load_balancer.load_balancer_attributes = lb_attributes
        context = AwsEnvironmentContext(load_balancers=[load_balancer])

        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
