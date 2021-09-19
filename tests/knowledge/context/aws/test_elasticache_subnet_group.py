from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestElastiCacheSubnetGroup(AwsContextTest):

    def get_component(self):
        return "elasticache/elasticache_subnet_group"

    @context(module_path="basic")
    def test_basic(self, ctx: AwsEnvironmentContext):
        subnet_group = next((subnet_group for subnet_group in ctx.elasticache_subnet_groups
                             if subnet_group.subnet_group_name == 'tf-test-cache-subnet'), None)
        self.assertIsNotNone(subnet_group)
        self.assertEqual(len(subnet_group.subnet_ids), 1)
        self.assertEqual(subnet_group.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/elasticache/home?region=us-east-1#cache-subnet-groups:names=tf-test-cache-subnet')
