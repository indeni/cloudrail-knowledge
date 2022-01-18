from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerClusterReleaseChannel
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_release_channel_enabled_rule import ContainerClusterReleaseChannelEnabledRule


class TestContainerClusterReleaseChannelEnabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterReleaseChannelEnabledRule()

    @parameterized.expand(
        [
            ["no_mode_specified", GcpContainerClusterReleaseChannel.UNSPECIFIED, 1, RuleResultType.FAILED],
            ["regular_mode", GcpContainerClusterReleaseChannel.REGULAR, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_release_channel_enabled(self, unused_name: str,
                                                      release_channel: GcpContainerClusterReleaseChannel,
                                                      total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        container_cluster.release_channel = release_channel
        context = GcpEnvironmentContext(container_clusters=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
