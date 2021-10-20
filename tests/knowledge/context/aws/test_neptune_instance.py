from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestNeptuneInstance(AwsContextTest):

    def get_component(self):
        return "neptune_instance"

    @context(module_path="vpc_non_default")
    def test_vpc_non_default(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.neptune_cluster_instances), 2)
        for neptune_instance in ctx.neptune_cluster_instances:
            self.assertTrue(neptune_instance.instance_identifier)
            self.assertTrue(neptune_instance.cluster_identifier)
            self.assertTrue(neptune_instance.arn)
            self.assertTrue(neptune_instance.name)
            self.assertEqual(neptune_instance.port, 8182)
            self.assertTrue(neptune_instance.network_configuration)
            self.assertFalse(neptune_instance.is_in_default_vpc)
            self.assertFalse(neptune_instance.tags)
            if not neptune_instance.is_managed_by_iac:
                validate_url = next((neptune_instance for neptune_instance in ctx.neptune_cluster_instances
                                     if neptune_instance.get_cloud_resource_url() == 'https://console.aws.amazon.com/neptune/home?region=us-east-1#'
                                     'database:id=tf-20210721090034115400000002;is-cluster=false'), None)
                self.assertIsNotNone(validate_url)
