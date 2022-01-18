from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_shielded_nodes_enabled_rule import ContainerClusterShieldedNodesEnabledRule


class TestContainerClusterShieldedNodesEnabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterShieldedNodesEnabledRule()

    @parameterized.expand(
        [
            ["disabled", False, 1, RuleResultType.FAILED],
            ["enabled", True, 0, RuleResultType.SUCCESS]
        ]
    )

    def test_container_cluster_shielded_nodes_enabled_rule(self, unused_name: str, enable_shielded_nodes: bool, total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster: GcpContainerCluster = create_empty_entity(GcpContainerCluster)
        container_cluster.enable_shielded_nodes = enable_shielded_nodes
        context = GcpEnvironmentContext(container_cluster=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
