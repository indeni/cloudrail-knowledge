from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


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
        region = 'us-east-2' if launch_config.origin == EntityOrigin.CLOUDFORMATION else 'us-east-1'
        self.assertEqual(launch_config.get_cloud_resource_url(),
                         f'https://console.aws.amazon.com/ec2autoscaling/home?region={region}#/lc?launchConfigurationName=web_config')
