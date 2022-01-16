from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerClusterShielededInstanceConfig
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_integrity_monitoring_shielded_nodes_enabled_rule import \
    ContainerClusterIntegrityMonitoringShieldedNodesEnabledRule


class TestContainerClusterIntegrityMonitoringShieldedNodesEnabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterIntegrityMonitoringShieldedNodesEnabledRule()

    @parameterized.expand(
        [
            ["disabled", False, 1, RuleResultType.FAILED],
            ["enabled", True, 0, RuleResultType.SUCCESS]
        ]
    )

    def test_container_cluster_secure_boot_shielded_nodes(self, unused_name: str, integrity_monitoring: bool, total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster: GcpContainerCluster = create_empty_entity(GcpContainerCluster)
        shielded_instance_config: GcpContainerClusterShielededInstanceConfig = create_empty_entity(GcpContainerClusterShielededInstanceConfig)
        shielded_instance_config.enable_integrity_monitoring = integrity_monitoring
        container_cluster.shielded_instance_config = shielded_instance_config
        context = GcpEnvironmentContext(container_cluster=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
