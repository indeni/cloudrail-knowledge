from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestMqBroker(AwsContextTest):

    def get_component(self):
        return 'mq_broker'

    @context(module_path="basic_default", base_scanner_data_for_iac='account-data-dms-instance-networking.zip')
    def test_basic_default(self, ctx: AwsEnvironmentContext):
        broker = next((broker for broker in ctx.mq_brokers if broker.broker_name == 'example'), None)
        self.assertIsNotNone(broker)
        self.assertTrue(broker.arn)
        self.assertTrue(broker.broker_id)
        self.assertEqual(broker.deployment_mode, 'SINGLE_INSTANCE')
        self.assertTrue(broker.get_all_network_configurations())
        self.assertFalse(broker.vpc_config.assign_public_ip)
        self.assertTrue(len(broker.vpc_config.subnet_list_ids) == 1)
        if not broker.is_managed_by_iac:
            self.assertEqual(broker.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/amazon-mq/home?region=us-east-1#/'
                             'brokers/details?id=b-77877260-4fad-4629-8d9e-93f9c113a6fb')
        self.assertTrue(len(broker.network_resource.network_interfaces) > 0)

    @context(module_path="default_vpc_multi_az", base_scanner_data_for_iac='account-data-dms-instance-networking.zip')
    def test_default_vpc_multi_az(self, ctx: AwsEnvironmentContext):
        broker = next((broker for broker in ctx.mq_brokers if broker.broker_name == 'example'), None)
        self.assertIsNotNone(broker)
        self.assertTrue(broker.arn)
        self.assertTrue(broker.broker_id)
        self.assertEqual(broker.deployment_mode, 'ACTIVE_STANDBY_MULTI_AZ')
        self.assertTrue(broker.get_all_network_configurations())
        self.assertFalse(broker.vpc_config.assign_public_ip)
        self.assertTrue(len(broker.vpc_config.subnet_list_ids) > 1)
        self.assertTrue(len(broker.network_resource.network_interfaces) > 0)

    @context(module_path="non_default_vpc")
    def test_non_default_vpc_multi_az(self, ctx: AwsEnvironmentContext):
        broker = next((broker for broker in ctx.mq_brokers if broker.broker_name == 'example'), None)
        self.assertIsNotNone(broker)
        self.assertTrue(broker.arn)
        self.assertTrue(broker.broker_id)
        self.assertEqual(broker.deployment_mode, 'ACTIVE_STANDBY_MULTI_AZ')
        self.assertTrue(broker.get_all_network_configurations())
        self.assertFalse(broker.vpc_config.assign_public_ip)
        self.assertTrue(len(broker.vpc_config.subnet_list_ids) > 1)
        self.assertTrue(len(broker.network_resource.network_interfaces) > 0)
