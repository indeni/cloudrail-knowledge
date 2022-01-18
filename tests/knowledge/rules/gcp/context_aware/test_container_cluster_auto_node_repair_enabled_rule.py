from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_node_pool import GcpContainerNodePool, GcpClusterNodePoolManagement
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.context_aware.container_cluster_auto_node_repair_enabled_rule import ContainerClusterAutoNodeRepairEnabledRule


class TestContainerClusterAutoNodeRepairEnabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterAutoNodeRepairEnabledRule()

    @parameterized.expand(
        [
            ["not_enabled", False, 1, RuleResultType.FAILED],
            ["enabled", True, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_auto_node_repair(self, unused_name: str, auto_repair: bool, total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster: GcpContainerCluster = create_empty_entity(GcpContainerCluster)
        node_pool: GcpContainerNodePool = create_empty_entity(GcpContainerNodePool)
        management: GcpClusterNodePoolManagement = create_empty_entity(GcpClusterNodePoolManagement)
        management.auto_repair = auto_repair
        node_pool.management = management
        container_cluster.node_pools.append(node_pool)
        context = GcpEnvironmentContext(container_clusters=[container_cluster],
                                        container_node_pools=[node_pool])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
