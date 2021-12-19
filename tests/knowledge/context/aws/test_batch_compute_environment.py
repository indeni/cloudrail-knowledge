from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestBatchComputeEnvironment(AwsContextTest):

    def get_component(self):
        return "batch_compute_environments"

    @context(module_path="managed_with_networking")
    def test_managed_with_networking(self, ctx: AwsEnvironmentContext):
        batch = next((batch for batch in ctx.batch_compute_environments if batch.server_name == 'sample'), None)
        self.assertIsNotNone(batch)
        self.assertTrue(batch.arn)
        self.assertTrue(batch.get_all_network_configurations())
        if not batch.is_managed_by_iac:
            self.assertEqual(batch.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/batch/v2/home?region=us-east-1#compute-environments/'
                             'detail/arn:aws:batch:us-east-1:115553109071:compute-environment/sample')
        self.assertTrue(batch.network_resource.security_groups)

    @context(module_path="basic_no_networking")
    def test_basic_no_networking(self, ctx: AwsEnvironmentContext):
        batch = next((batch for batch in ctx.batch_compute_environments if batch.server_name == 'sample'), None)
        self.assertIsNotNone(batch)
        self.assertTrue(batch.arn)
        self.assertFalse(batch.get_all_network_configurations())
