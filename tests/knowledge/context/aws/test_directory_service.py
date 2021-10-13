import unittest

from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestDirectoryService(AwsContextTest):

    def get_component(self):
        return "directory_service"

    @context(module_path="basic")
    def test_basic(self, ctx: AwsEnvironmentContext):
        directory = next((directory for directory in ctx.cloud_directories if directory.name == 'corp.notexample.com'), None)
        self.assertIsNotNone(directory)
        self.assertTrue(directory.directory_id)
        self.assertTrue(directory.vpc_config)
        self.assertTrue(directory.vpc_id)
        self.assertEqual(directory.directory_type, 'SimpleAD')
        self.assertTrue(directory.get_all_network_configurations())
        self.assertTrue(directory.security_group_controller)
        self.assertIsInstance(directory.security_group_controller, SecurityGroup)
        if not directory.is_managed_by_iac:
            self.assertEqual(directory.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/directoryservicev2/home?region=us-east-1#!/directories/d-906769fc67')

    @unittest.skip('Unable to test AD connector, as real DNS server is required for testing')
    @context(module_path="ad_connector")
    def test_ad_connector(self, ctx: AwsEnvironmentContext):
        directory = next((directory for directory in ctx.cloud_directories if directory.name == 'corp.notexample.com'), None)
        self.assertIsNotNone(directory)
        self.assertTrue(directory.directory_id)
        self.assertTrue(directory.vpc_config)
        self.assertTrue(directory.vpc_id)
        self.assertEqual(directory.directory_type, 'ADConnector')
        self.assertTrue(directory.get_all_network_configurations())
