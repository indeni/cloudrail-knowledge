from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerClusterWorkloadMetadataConfigMode
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_metadata_server_enabled_rule import ContainerClusterMetadataServerEnabledRule


class TestContainerClusterMetadataServerEnabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterMetadataServerEnabledRule()

    @parameterized.expand(
        [
            ["no_mode_specified", GcpContainerClusterWorkloadMetadataConfigMode.MODE_UNSPECIFIED, 1, RuleResultType.FAILED],
            ["gck_metadata", GcpContainerClusterWorkloadMetadataConfigMode.GKE_METADATA, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_metadata_server_enabled(self, unused_name: str,
                                                      workload_metadata_config_mode: GcpContainerClusterWorkloadMetadataConfigMode,
                                                      total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        container_cluster.workload_metadata_config_mode = workload_metadata_config_mode
        context = GcpEnvironmentContext(container_cluster=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
