from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeSubNetwork(GcpContextTest):
    def get_component(self):
        return 'compute_subnetwork'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        subnetwork = next((subnetwork for subnetwork in ctx.compute_subnetworks if subnetwork.name == 'log-test-subnetwork'), None)
        self.assertIsNotNone(subnetwork)
        self.assertIsNotNone(subnetwork.network)
        self.assertIsNotNone(subnetwork.log_config)
        self.assertEqual(subnetwork.log_config.aggregation_interval, "INTERVAL_10_MIN")
        self.assertEqual(subnetwork.log_config.flow_sampling, 0.5)
        self.assertEqual(subnetwork.log_config.metadata, "INCLUDE_ALL_METADATA")
        self.assertEqual(subnetwork.ip_cidr_range, "10.2.0.0/16")

        if subnetwork.origin == EntityOrigin.TERRAFORM:
            self.assertEqual(subnetwork.network_identifier, "google_compute_network.custom-test.id")
            self.assertIsNone(subnetwork.region)
        elif subnetwork.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(subnetwork.network_identifier, "https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/networks/log-test-network")
            self.assertEqual(subnetwork.region, "us-west1")
