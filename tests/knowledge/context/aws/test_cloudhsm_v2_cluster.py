from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_hsm import CloudHsmV2Hsm
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestCloudHsmV2Cluster(AwsContextTest):

    def get_component(self):
        return "cloudhsm_v2_cluster"

    @context(module_path="basic", test_options=TestOptions(run_cloudmapper=False))
    def test_basic(self, ctx: AwsEnvironmentContext):
        cluster = next((cluster for cluster in ctx.cloudhsm_v2_clusters if cluster.hsm_type == 'hsm1.medium'), None)
        self.assertIsNotNone(cluster)
        self.assertTrue(len(cluster.subnet_ids), 2)
        self.assertTrue(cluster.cluster_id)
        self.assertTrue(cluster.vpc_id)
        self.assertTrue(cluster.security_group_id)
        self.assertIsNotNone(cluster.cluster_hsm)
        self.assertIsInstance(cluster.cluster_hsm, CloudHsmV2Hsm)
        hsm = next((hsm for hsm in ctx.cloudhsm_list if hsm.cluster_id == cluster.cluster_id), None)
        self.assertIsNotNone(hsm)
        self.assertTrue(len(hsm.subnet_id), 1)
        self.assertTrue(hsm.hsm_id)
        self.assertTrue(hsm.hsm_state)
        self.assertTrue(hsm.availability_zone)
