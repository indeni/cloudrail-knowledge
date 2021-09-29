import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_attributes import LoadBalancerAccessLogs, LoadBalancerAttributes
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_load_balancer_logging_enabeld_rule import \
    EnsureLoadBalancerLoggingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureLoadBalancerLoggingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLoadBalancerLoggingEnabledRule()

    def test_non_car_elb_logging_enabled_fail(self):
        # Arrange
        load_balancer: LoadBalancer = create_empty_entity(LoadBalancer)
        lb_attributes: LoadBalancerAttributes = create_empty_entity(LoadBalancerAttributes)
        access_logs: LoadBalancerAccessLogs = create_empty_entity(LoadBalancerAccessLogs)
        access_logs.enabled = False
        lb_attributes.access_logs = access_logs
        load_balancer.load_balancer_attributes = lb_attributes
        context = AwsEnvironmentContext(load_balancers=[load_balancer])

        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_elb_logging_enabled_pass(self):
        # Arrange
        load_balancer: LoadBalancer = create_empty_entity(LoadBalancer)
        lb_attributes: LoadBalancerAttributes = create_empty_entity(LoadBalancerAttributes)
        access_logs: LoadBalancerAccessLogs = create_empty_entity(LoadBalancerAccessLogs)
        access_logs.enabled = True
        lb_attributes.access_logs = access_logs
        load_balancer.load_balancer_attributes = lb_attributes
        context = AwsEnvironmentContext(load_balancers=[load_balancer])

        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
