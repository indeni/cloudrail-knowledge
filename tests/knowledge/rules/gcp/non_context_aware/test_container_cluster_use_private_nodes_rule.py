from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerClusterPrivateClusterConfig
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_use_private_nodes_rule import ContainerClusterUsePrivateNodesRule


class TestContainerClusterUsePrivateNodesRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterUsePrivateNodesRule()

    @parameterized.expand(
        [
            ["no_private_config", False, None, 1, RuleResultType.FAILED],
            ["with_private_config_private_nodes_disabled", True, False, 1, RuleResultType.FAILED],
            ["with_private_config_private_nodes_enabled", True, True, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_use_private_nodes(self, unused_name: str, private_cluster_configuration: bool,
                                                 enable_private_nodes: bool, total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster: GcpContainerCluster = create_empty_entity(GcpContainerCluster)
        private_cluster_config: GcpContainerClusterPrivateClusterConfig = create_empty_entity(GcpContainerClusterPrivateClusterConfig)
        if private_cluster_configuration:
            private_cluster_config.enable_private_nodes = enable_private_nodes
            container_cluster.private_cluster_config = private_cluster_config
        context = GcpEnvironmentContext(container_clusters=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
