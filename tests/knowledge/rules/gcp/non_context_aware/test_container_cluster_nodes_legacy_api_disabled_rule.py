from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster_node_config import GcpContainerClusterNodeConfig
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_nodes_legacy_api_disabled_rule import ContainerClusterNodesLegacyApiDisabledRule


class TestContainerClusterNodesLegacyApiDisabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterNodesLegacyApiDisabledRule()

    @parameterized.expand(
        [
            ["enabled", {'disable-legacy-endpoints': 'false'}, 1, RuleResultType.FAILED],
            ["disabled", {'disable-legacy-endpoints': 'true'}, 0, RuleResultType.SUCCESS]
        ]
    )

    def test_container_cluster_legacy_api_nodes(self, unused_name: str, metadata: dict, total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        node_config: GcpContainerClusterNodeConfig = create_empty_entity(GcpContainerClusterNodeConfig)
        node_config.metadata = metadata
        container_cluster.node_config = node_config
        context = GcpEnvironmentContext(container_clusters=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
