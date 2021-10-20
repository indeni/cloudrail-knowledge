from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestLaunchTemplates(AwsContextTest):

    def get_component(self):
        return "launch_templates"

    @context(module_path="basic_http_token_required")
    def test_basic_http_token_required(self, ctx: AwsEnvironmentContext):
        launch_template = ctx.launch_templates[0]
        self.assertEqual(launch_template.http_token, 'required')
        self.assertTrue(launch_template.template_id)
        self.assertEqual(launch_template.instance_type, 't2.micro')
        self.assertFalse(launch_template.monitoring_enabled)
        self.assertFalse(launch_template.ebs_optimized)
        self.assertEqual(launch_template.name, 'launch_template_test')
        if not launch_template.is_managed_by_iac:
            self.assertEqual(launch_template.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#'
                             'LaunchTemplateDetails:launchTemplateId=lt-085c2de968aadd64b')

    @context(module_path="http_token_optional")
    def test_http_token_optional(self, ctx: AwsEnvironmentContext):
        launch_template = ctx.launch_templates[0]
        self.assertEqual(launch_template.http_token, 'optional')
        self.assertTrue(launch_template.template_id)
        self.assertEqual(launch_template.name, 'launch_template_test')
        self.assertEqual(launch_template.instance_type, 't2.micro')
        self.assertTrue(launch_template.monitoring_enabled)
        self.assertTrue(launch_template.ebs_optimized)
