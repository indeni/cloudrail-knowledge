from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestLaunchConfigurations(AwsContextTest):

    def get_component(self):
        return "launch_configurations"

    @context(module_path="launch_configuration_http_token_optional")
    def test_launch_configuration_http_token_optional(self, ctx: AwsEnvironmentContext):
        launch_config = ctx.launch_configurations[0]
        self.assertEqual(launch_config.http_tokens, 'optional')
        self.assertTrue(launch_config.ebs_optimized)
        self.assertTrue(launch_config.monitoring_enabled)
        self.assertEqual(launch_config.instance_type, 't2.micro')
        self.assertEqual(launch_config.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/ec2autoscaling/home?region=us-east-1#/lc?launchConfigurationName=web_config')
