import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer, LoadBalancerType
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target import LoadBalancerTarget
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group import LoadBalancerTargetGroup
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.alb_disallow_target_groups_http_rule import AlbDisallowHttpRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAlbDisallowHttpRule(unittest.TestCase):
    def setUp(self):
        self.rule = AlbDisallowHttpRule()

    def test_non_car_alb_target_group_no_http_fail(self):
        # Arrange
        load_balancer: LoadBalancer = create_empty_entity(LoadBalancer)
        load_balancer.load_balancer_type = LoadBalancerType.APPLICATION
        lb_target_group: LoadBalancerTargetGroup = create_empty_entity(LoadBalancerTargetGroup)
        lb_target_group.protocol = 'HTTP'
        lb_target: LoadBalancerTarget = create_empty_entity(LoadBalancerTarget)
        lb_target_group.targets = [lb_target]
        load_balancer.target_groups = [lb_target_group]
        context = AwsEnvironmentContext(load_balancers=[load_balancer],
                                        load_balancer_targets=[lb_target],
                                        load_balancer_target_groups=[lb_target_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_alb_target_group_no_http__network_lb__pass(self):
        # Arrange
        load_balancer: LoadBalancer = create_empty_entity(LoadBalancer)
        load_balancer.load_balancer_type = LoadBalancerType.NETWORK
        lb_target_group: LoadBalancerTargetGroup = create_empty_entity(LoadBalancerTargetGroup)
        lb_target_group.protocol = 'HTTP'
        lb_target: LoadBalancerTarget = create_empty_entity(LoadBalancerTarget)
        lb_target_group.targets = [lb_target]
        load_balancer.target_groups = [lb_target_group]
        context = AwsEnvironmentContext(load_balancers=[load_balancer])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_alb_target_group_no_http__not_http_protocol__pass(self):
        # Arrange
        load_balancer: LoadBalancer = create_empty_entity(LoadBalancer)
        load_balancer.load_balancer_type = LoadBalancerType.APPLICATION
        lb_target_group: LoadBalancerTargetGroup = create_empty_entity(LoadBalancerTargetGroup)
        lb_target_group.protocol = 'HTTPS'
        lb_target: LoadBalancerTarget = create_empty_entity(LoadBalancerTarget)
        lb_target_group.targets = [lb_target]
        load_balancer.target_groups = [lb_target_group]
        context = AwsEnvironmentContext(load_balancers=[load_balancer])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
