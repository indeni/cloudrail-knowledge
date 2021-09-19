from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestEks(AwsContextTest):

    def get_component(self):
        return "eks"

    @context(module_path="basic", test_options=TestOptions(tf_version='>=3.10'))
    def test_basic_eks(self, ctx: AwsEnvironmentContext):
        cluster = ctx.eks_clusters[0]
        self.assertTrue(cluster.endpoint_public_access)
        self.assertFalse(cluster.endpoint_private_access)
        self.assertEqual(cluster.name, 'my-cluster')
        self.assertEqual(len(cluster.network_resource.network_interfaces), 3)
        self.assertEqual(len(cluster.network_resource.subnets), 3)
        self.assertGreaterEqual(len(cluster.network_resource.public_ip_addresses), 1)
        self.assertEqual(len(cluster.network_resource.security_groups), 2)
        self.assertTrue(cluster.cluster_security_group_id)
        self.assertFalse(cluster.tags)
        if not cluster.is_managed_by_iac:
            self.assertEqual(cluster.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/eks/home?region=eu-west-1#/clusters/my-cluster')

    @context(module_path='eks_on_default_subnet')
    def test_eks_on_default_subnet(self, ctx: AwsEnvironmentContext):
        cluster = ctx.eks_clusters[0]
        self.assertTrue(cluster.endpoint_public_access)
        self.assertFalse(cluster.endpoint_private_access)
        self.assertEqual(cluster.name, 'test')
        self.assertEqual(len(cluster.network_resource.network_interfaces), 2)
        self.assertEqual(len(cluster.network_resource.subnets), 2)
        self.assertGreaterEqual(len(cluster.network_resource.public_ip_addresses), 2)
        self.assertEqual(len(cluster.network_resource.security_groups), 1)
        self.assertTrue(cluster.cluster_security_group_id)

    @context(module_path="cr-1625")
    def test_cr_1625(self, ctx: AwsEnvironmentContext):
        cluster = ctx.eks_clusters[0]
        self.assertEqual(cluster.public_access_cidrs, ['0.0.0.0/0'])
        for statement in ctx.roles[0].permissions_policies[0].statements:
            self.assertFalse(any(action is None for action in statement.actions))
