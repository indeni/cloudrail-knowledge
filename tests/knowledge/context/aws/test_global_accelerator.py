from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestGlobalAccelerator(AwsContextTest):

    def get_component(self):
        return "global_accelerator"

    @context(module_path="with_associated_security_group", test_options=TestOptions(tf_version='>3.4.0'))
    def test_with_associated_security_group_global_ac(self, ctx: AwsEnvironmentContext):
        global_ac = next((ac for ac in ctx.global_accelerators if ac.accelerator_name == 'ga-test'), None)
        self.assertIsNotNone(global_ac)
        self.assertTrue(global_ac.arn)
        self.assertEqual(global_ac.region, 'us-west-2')
        if not global_ac.is_managed_by_iac:
            self.assertEqual(global_ac.get_cloud_resource_url(),
                             'https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#AcceleratorDetails:AcceleratorArn=arn:aws:'
                             'globalaccelerator::115553109071:accelerator/5c917162-0f7b-449d-8285-1431e2bce96a')

    @context(module_path="with_associated_security_group", test_options=TestOptions(tf_version='>3.4.0'))
    def test_with_associated_security_group_listener(self, ctx: AwsEnvironmentContext):
        listener = next((listener for listener in ctx.global_accelerator_listeners
                         if listener.accelerator_arn == 'aws_globalaccelerator_accelerator.test.id'
                         or listener.accelerator_arn == 'arn:aws:globalaccelerator::115553109071:accelerator/'
                                                        '5c917162-0f7b-449d-8285-1431e2bce96a'), None)
        self.assertIsNotNone(listener)
        self.assertTrue(listener.listener_arn)
        self.assertEqual(listener.region, 'us-west-2')
        if not listener.is_managed_by_iac:
            self.assertEqual(listener.get_cloud_resource_url(),
                             'https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#ListenerDetails:ListenerArn=arn:aws:'
                             'globalaccelerator::115553109071:accelerator/5c917162-0f7b-449d-8285-1431e2bce96a/listener/4ceecded')

    @context(module_path="with_associated_security_group", base_scanner_data_for_iac='account-data-emr-networking',
             test_options=TestOptions(tf_version='>3.4.0'))
    def test_with_associated_security_group_endpoint(self, ctx: AwsEnvironmentContext):
        endpoint = next((endpoint for endpoint in ctx.global_accelerator_endpoint_groups
                         if endpoint.listener_arn == 'aws_globalaccelerator_listener.test.id'
                         or endpoint.listener_arn == 'arn:aws:globalaccelerator::115553109071:accelerator/5c917162-0f7b-449d-8285-1431e2bce96a/'
                                                     'listener/4ceecded'), None)
        self.assertIsNotNone(endpoint)
        self.assertTrue(endpoint.listener_arn)
        self.assertEqual(endpoint.region, 'us-east-1')
        self.assertTrue(endpoint.endpoint_config_id)
        self.assertTrue(endpoint.client_ip_preservation_enabled)
        self.assertTrue(isinstance(endpoint.endpoint_resource, LoadBalancer))
        if not endpoint.is_managed_by_iac:
            self.assertEqual(endpoint.get_cloud_resource_url(),
                             'https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#EndpointGroupDetails:EndpointGroupArn=arn:aws:'
                             'globalaccelerator::115553109071:accelerator/5c917162-0f7b-449d-8285-1431e2bce96a/'
                             'listener/4ceecded/endpoint-group/e2338bc6b002')

    @context(module_path="elastic_ip_endpoint", base_scanner_data_for_iac='account-data-emr-networking', test_options=TestOptions(tf_version='>3.4.0'))
    def test_elastic_ip_endpoint(self, ctx: AwsEnvironmentContext):
        endpoint = next((endpoint for endpoint in ctx.global_accelerator_endpoint_groups
                         if endpoint.listener_arn == 'aws_globalaccelerator_listener.test.id'
                         or endpoint.listener_arn == 'arn:aws:globalaccelerator::115553109071:accelerator/8fb6e17b-d2f6-4bce-8746-f6e2a9bf3264/'
                                                     'listener/22ce44b7'), None)
        self.assertIsNotNone(endpoint)
        self.assertTrue(endpoint.listener_arn)
        self.assertEqual(endpoint.region, 'us-east-1')
        self.assertTrue(endpoint.endpoint_config_id)
        self.assertFalse(endpoint.client_ip_preservation_enabled)
        self.assertTrue(isinstance(endpoint.endpoint_resource, ElasticIp))

    @context(module_path="ec2_endpoint", base_scanner_data_for_iac='account-data-emr-networking', test_options=TestOptions(tf_version='>3.4.0'))
    def test_ec2_endpoint(self, ctx: AwsEnvironmentContext):
        endpoint = next((endpoint for endpoint in ctx.global_accelerator_endpoint_groups
                         if endpoint.listener_arn == 'aws_globalaccelerator_listener.test.id'
                         or endpoint.listener_arn == 'arn:aws:globalaccelerator::115553109071:accelerator/1c878acf-ffe2-41bc-ba6b-682b72dda6fc/'
                                                     'listener/19f9c87e'), None)
        self.assertIsNotNone(endpoint)
        self.assertTrue(endpoint.listener_arn)
        self.assertEqual(endpoint.region, 'us-east-1')
        self.assertTrue(endpoint.endpoint_config_id)
        self.assertTrue(endpoint.client_ip_preservation_enabled)
        self.assertTrue(isinstance(endpoint.endpoint_resource, Ec2Instance))

    @context(module_path="global_accelerator_with_flow_logs", base_scanner_data_for_iac='account-data-emr-networking',
             test_options=TestOptions(tf_version='>3.4.0'))
    def test_global_accelerator_with_flow_logs(self, ctx: AwsEnvironmentContext):
        attributes = next((attribute for attribute in ctx.global_accelerator_attributes
                           if attribute.accelerator_arn == 'aws_globalaccelerator_accelerator.test.id'
                           or attribute.accelerator_arn == 'arn:aws:globalaccelerator::115553109071:accelerator/'
                                                           '1a29e4cd-336a-40d0-982e-02129892ab01'), None)
        self.assertIsNotNone(attributes)
        self.assertTrue(attributes.flow_logs_enabled)
        self.assertTrue(attributes.flow_logs_s3_bucket)
        self.assertEqual(attributes.flow_logs_s3_prefix, 'flow-logs/')

    @context(module_path="flow_logs_disabled", base_scanner_data_for_iac='account-data-emr-networking',
             test_options=TestOptions(tf_version='>3.4.0'))
    def test_flow_logs_disabled(self, ctx: AwsEnvironmentContext):
        attributes = next((attribute for attribute in ctx.global_accelerator_attributes
                           if attribute.accelerator_arn == 'aws_globalaccelerator_accelerator.test.id'
                           or attribute.accelerator_arn == 'arn:aws:globalaccelerator::115553109071:accelerator/'
                                                           'c4ca165d-3fdc-4c26-b242-a7985ea0c987'), None)
        self.assertIsNotNone(attributes)
        self.assertFalse(attributes.flow_logs_enabled)
        self.assertTrue(attributes.flow_logs_s3_bucket)
        self.assertEqual(attributes.flow_logs_s3_prefix, 'flow-logs/')

    @context(module_path="no_flow_logs_configured", base_scanner_data_for_iac='account-data-emr-networking',
             test_options=TestOptions(tf_version='>3.4.0'))
    def test_no_flow_logs_configured(self, ctx: AwsEnvironmentContext):
        gac = next((gac for gac in ctx.global_accelerators
                    if gac.arn == 'aws_globalaccelerator_accelerator.test.id'
                    or gac.arn == 'arn:aws:globalaccelerator::115553109071:accelerator/36d00926-4a42-4299-98ff-9cda591fa7c0'), None)
        self.assertIsNotNone(gac)
        self.assertFalse(gac.attributes.flow_logs_enabled)
        self.assertIsNone(gac.attributes.flow_logs_s3_bucket)
        self.assertIsNone(gac.attributes.flow_logs_s3_prefix)
