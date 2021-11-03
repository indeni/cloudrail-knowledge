from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestLoadBalancerAttributes(AwsContextTest):

    def get_component(self):
        return 'load_balancer_attributes'

    @context(module_path="invalid_headers_enabled")
    def test_invalid_headers_enabled(self, ctx: AwsEnvironmentContext):
        lb = next((lb for lb in ctx.load_balancers_attributes
                   if lb.load_balancer_arn == 'arn:aws:elasticloadbalancing:us-east-1:115553109071:loadbalancer/app/test-lb-drop/d3a781a0bec2e5b8'
                   or lb.load_balancer_arn == 'aws_lb.test.arn'), None)
        self.assertIsNotNone(lb)
        self.assertTrue(lb.drop_invalid_header_fields)

    @context(module_path="invalid_headers_disabled")
    def test_invalid_headers_disabled(self, ctx: AwsEnvironmentContext):
        lb = next((lb for lb in ctx.load_balancers_attributes
                   if lb.load_balancer_arn == 'arn:aws:elasticloadbalancing:us-east-1:115553109071:loadbalancer/app/test-lb-no-drop/0c8374a3f80f9d4c'
                   or lb.load_balancer_arn == 'aws_lb.test.arn'), None)
        self.assertIsNotNone(lb)
        self.assertFalse(lb.drop_invalid_header_fields)

    @context(module_path="invalid_headers_enabled_lb_resource", base_scanner_data_for_iac='account-data-dms-instance-networking-public.zip')
    def test_invalid_headers_enabled_lb_resource(self, ctx: AwsEnvironmentContext):
        lb = next((lb for lb in ctx.load_balancers
                   if lb.load_balancer_arn == 'arn:aws:elasticloadbalancing:us-east-1:115553109071:loadbalancer/app/test-lb-drop/d3a781a0bec2e5b8'
                   or lb.load_balancer_arn == 'aws_lb.test.arn'), None)
        self.assertIsNotNone(lb)
        self.assertTrue(lb.load_balancer_attributes.drop_invalid_header_fields)
        self.assertFalse(lb.load_balancer_attributes.access_logs.enabled)
        self.assertEqual(lb.load_balancer_attributes.access_logs.prefix, '')
        self.assertEqual(lb.load_balancer_attributes.access_logs.bucket, '')

    @context(module_path="lb_with_access_logs", base_scanner_data_for_iac='account-data-dms-instance-networking-public.zip')
    def test_lb_with_access_logs(self, ctx: AwsEnvironmentContext):
        lb = next((lb for lb in ctx.load_balancers
                   if lb.load_balancer_arn == 'arn:aws:elasticloadbalancing:us-east-1:115553109071:loadbalancer/app/lb-test-logging/c51ae407bfd2ae3c'
                   or lb.load_balancer_arn == 'aws_lb.test.arn'), None)
        self.assertIsNotNone(lb)
        self.assertTrue(lb.load_balancer_attributes.access_logs)
        self.assertTrue(lb.load_balancer_attributes.access_logs.enabled)
        self.assertEqual(lb.load_balancer_attributes.access_logs.prefix, 'elb')
        self.assertTrue(lb.load_balancer_attributes.access_logs.bucket)

    @context(module_path="lb_access_logs_disabled", base_scanner_data_for_iac='account-data-dms-instance-networking-public.zip')
    def test_lb_access_logs_disabled(self, ctx: AwsEnvironmentContext):
        lb = next((lb for lb in ctx.load_balancers
                   if lb.load_balancer_arn == 'arn:aws:elasticloadbalancing:us-east-1:115553109071:loadbalancer/app/lb-test-logging/acb800d9129a6270'
                   or lb.load_balancer_arn == 'aws_lb.test.arn'), None)
        self.assertIsNotNone(lb)
        self.assertTrue(lb.load_balancer_attributes.access_logs)
        self.assertFalse(lb.load_balancer_attributes.access_logs.enabled)
        if not lb.is_managed_by_iac:
            self.assertEqual(lb.load_balancer_attributes.access_logs.prefix, '')
            self.assertEqual(lb.load_balancer_attributes.access_logs.bucket, '')
        else:
            self.assertEqual(lb.load_balancer_attributes.access_logs.prefix, 'elb')
            self.assertEqual(lb.load_balancer_attributes.access_logs.bucket, 'aws_s3_bucket.logging.bucket')
