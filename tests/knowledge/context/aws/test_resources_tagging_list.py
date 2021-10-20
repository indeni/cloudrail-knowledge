from tests.knowledge.context.aws_context_test import AwsContextTest
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestResourceTagMappingList(AwsContextTest):

    def get_component(self):
        return 'resources_tagging_list'

    @context(module_path='basic', test_options=TestOptions(run_terraform=False, run_drift_detection=False))
    def test_basic(self, ctx: AwsEnvironmentContext):
        self.assertEqual(208, len(ctx.resources_tagging_list))
        resource_with_tags = next((resource for resource in ctx.resources_tagging_list
                                   if resource.resource_arn == 'arn:aws:lambda:us-east-1:115553109071:function:assessment_get-dev-imanuel'), None)
        self.assertIsNotNone(resource_with_tags)
        self.assertTrue(resource_with_tags.tags)
        resource_without_tags = next((resource for resource in ctx.resources_tagging_list
                                      if not resource.tags), None)
        self.assertIsNotNone(resource_without_tags)
        self.assertEqual(resource_without_tags.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/resource-groups/tag-editor/find-resources?region=us-east-1')
