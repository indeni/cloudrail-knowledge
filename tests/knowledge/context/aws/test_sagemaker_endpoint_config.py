from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestSageMakerEndpointConfig(AwsContextTest):

    def get_component(self):
        return "sagemaker"

    @context(module_path="sagemaker_endpoint_config_encrypted")
    def test_sagemaker_endpoint_config_encrypted(self, ctx: AwsEnvironmentContext):
        sagemaker_endpoint_config = next((sage for sage in ctx.sagemaker_endpoint_config_list
                                          if sage.sagemaker_endpoint_config_name == 'my-endpoint-config'), None)
        self.assertIsNotNone(sagemaker_endpoint_config)
        self.assertTrue(sagemaker_endpoint_config.encrypted)
        self.assertTrue(sagemaker_endpoint_config.arn)
        self.assertEqual(sagemaker_endpoint_config.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/sagemaker/home?region=us-east-1#/endpointConfig/my-endpoint-config')

    @context(module_path="sagemaker_endpoint_config_non_encrypted")
    def test_sagemaker_endpoint_config_non_encrypted(self, ctx: AwsEnvironmentContext):
        sagemaker_endpoint_config = next((sage for sage in ctx.sagemaker_endpoint_config_list
                                          if sage.sagemaker_endpoint_config_name == 'my-endpoint-config'), None)
        self.assertIsNotNone(sagemaker_endpoint_config)
        self.assertFalse(sagemaker_endpoint_config.encrypted)
        self.assertTrue(sagemaker_endpoint_config.arn)
