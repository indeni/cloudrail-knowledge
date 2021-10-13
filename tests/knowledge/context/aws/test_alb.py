from typing import List

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer, LoadBalancerSchemeType, LoadBalancerType

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestAlb(AwsContextTest):

    def get_component(self):
        return "alb"

    @context(module_path="defaults_only_app_lb")
    def test_defaults_only_app_lb(self, ctx: AwsEnvironmentContext):
        alb = self._assert_and_get_lb(ctx, LoadBalancerType.APPLICATION, LoadBalancerSchemeType.INTERNET_FACING)
        self.assertEqual(alb.get_cloud_resource_url(), 'https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LoadBalancers')
        self._assert_subnets(alb)

    @context(module_path="defaults_only_network_lb")
    def test_defaults_only_network_lb(self, ctx: AwsEnvironmentContext):
        nlb = self._assert_and_get_lb(ctx, LoadBalancerType.NETWORK, LoadBalancerSchemeType.INTERNET_FACING)
        self._assert_subnets(nlb)

    @context(module_path="simple_basic_case_with_default_subnet")
    def test_simple_basic_case_with_default_subnet(self, ctx: AwsEnvironmentContext):
        alb = self._assert_and_get_lb(ctx, LoadBalancerType.APPLICATION, LoadBalancerSchemeType.INTERNET_FACING)
        self._assert_subnets(alb, False)
        self.assertTrue(all(subnet.is_default for subnet in alb.network_resource.subnets))
        self.assertTrue(alb.network_resource.subnets[0].vpc.is_default)

    @context(module_path="simple_basic_case")
    def test_simple_basic_case(self, ctx: AwsEnvironmentContext):
        alb = self._assert_and_get_lb(ctx, LoadBalancerType.APPLICATION, LoadBalancerSchemeType.INTERNET_FACING)
        self._assert_subnets(alb)
        self.assertTrue(any(sg for sg in alb.network_resource.security_groups if sg.is_default))
        self.assertTrue(len(alb.network_resource.public_ip_addresses) > 0)

    @context(module_path="simple_basic_case_with_subnet_mapping")
    def test_simple_basic_case_with_subnet_mapping(self, ctx: AwsEnvironmentContext):
        nlb = self._assert_and_get_lb(ctx, LoadBalancerType.NETWORK, LoadBalancerSchemeType.INTERNET_FACING)
        self._assert_subnets(nlb)
        self.assertTrue(len(nlb.network_resource.public_ip_addresses) > 0)

    @context(module_path="internal_case")
    def test_internal_case(self, ctx: AwsEnvironmentContext):
        alb = self._assert_and_get_lb(ctx, LoadBalancerType.APPLICATION, LoadBalancerSchemeType.INTERNAL, [80])
        self._assert_subnets(alb)
        self.assertTrue(len([sg for sg in alb.network_resource.security_groups if sg.is_default]) > 0)
        self.assertFalse(len(alb.network_resource.public_ip_addresses) > 0)
        self.assertFalse(alb.tags)

        # Now Target Group
        self.assertTrue(len(ctx.load_balancer_target_groups) > 0)
        self.assertTrue(len(alb.target_groups) > 0)
        self.assertFalse(alb.target_groups[0].tags)

        # Now actual targets (expecting the instance)
        self.assertTrue(len(alb.target_groups[0].targets) == 1)
        self.assertTrue(len(ctx.ec2s) == 1)
        self.assertEqual(ctx.ec2s[0], alb.target_groups[0].targets[0].target_instance)

    @context(module_path="network-lb-no-sg")
    def test_network_lb_no_sg(self, ctx: AwsEnvironmentContext):
        nlb = self._assert_and_get_lb(ctx, LoadBalancerType.NETWORK, LoadBalancerSchemeType.INTERNET_FACING)
        self.assertEqual(len(nlb.network_resource.subnets), 1)

        # It's a network LB, no security groups, ever
        self.assertEqual(0, len(nlb.raw_data.security_groups_ids))

    def _assert_and_get_lb(self, ctx: AwsEnvironmentContext, lb_type: LoadBalancerType,
                           scheme_type: LoadBalancerSchemeType, listener_ports: List[int] = None):
        listener_ports = listener_ports or []
        self.assertEqual(len(ctx.load_balancers), 1)
        lb = ctx.load_balancers[0]
        self.assertEqual(lb_type, lb.load_balancer_type)
        self.assertEqual(scheme_type, lb.scheme_type)
        self.assertEqual(len(listener_ports), len(lb.listener_ports))
        self.assertTrue(all(port in listener_ports for port in lb.listener_ports))
        return lb

    def _assert_subnets(self, lb: LoadBalancer, assert_names: bool = True):
        self.assertEqual(2, len(lb.network_resource.subnets))
        if assert_names:
            self.assertTrue(any(subnet.name == 'subnet1' for subnet in lb.network_resource.subnets))
            self.assertTrue(any(subnet.name == 'subnet2' for subnet in lb.network_resource.subnets))

    @context(module_path="with_tags")
    def test_internal_case_with_tags(self, ctx: AwsEnvironmentContext):
        alb = self._assert_and_get_lb(ctx, LoadBalancerType.APPLICATION, LoadBalancerSchemeType.INTERNAL, [80])
        self.assertIsNotNone(alb)
        self.assertTrue(alb.tags)
        for target_group in alb.target_groups:
            self.assertTrue(target_group.tags)
