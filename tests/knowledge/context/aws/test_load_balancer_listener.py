from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestLoadBalancerListener(AwsContextTest):

    def get_component(self):
        return 'load_balancer_listeners'

    @context(module_path="http")
    def test_http_listener(self, ctx: AwsEnvironmentContext):
        distribution = ctx.load_balancer_listeners[0]
        self.assertEqual(distribution.listener_protocol, 'HTTP')
        self.assertEqual(distribution.listener_port, 80)
        self.assertEqual(distribution.default_action_type, 'forward')
        self.assertFalse(distribution.redirect_action_protocol)
        self.assertFalse(distribution.redirect_action_port)

    @context(module_path="https")
    def test_https_listener(self, ctx: AwsEnvironmentContext):
        distribution = ctx.load_balancer_listeners[0]
        self.assertEqual(distribution.listener_protocol, 'HTTPS')
        self.assertEqual(distribution.listener_port, 443)
        self.assertEqual(distribution.default_action_type, 'forward')
        self.assertFalse(distribution.redirect_action_protocol)
        self.assertFalse(distribution.redirect_action_port)
        self.assertEqual(distribution.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LoadBalancers:type=application')

    @context(module_path="http_redirect_type")
    def test_http_listener_with_redirect(self, ctx: AwsEnvironmentContext):
        distribution = ctx.load_balancer_listeners[0]
        self.assertEqual(distribution.listener_protocol, 'HTTP')
        self.assertEqual(distribution.listener_port, 80)
        self.assertEqual(distribution.default_action_type, 'redirect')
        self.assertEqual(distribution.redirect_action_protocol, 'HTTPS')
        self.assertEqual(distribution.redirect_action_port, '443')

    @context(module_path="load_balancer_listener_http_redirect_http_url_port")
    def test_load_balancer_listener_http_redirect_http_url_port(self, ctx: AwsEnvironmentContext):
        distribution = ctx.load_balancer_listeners[0]
        self.assertEqual(distribution.listener_protocol, 'HTTP')
        self.assertEqual(distribution.listener_port, 80)
        self.assertEqual(distribution.default_action_type, 'redirect')
        self.assertEqual(distribution.redirect_action_protocol, 'HTTP')
        self.assertEqual(distribution.redirect_action_port, 80)
