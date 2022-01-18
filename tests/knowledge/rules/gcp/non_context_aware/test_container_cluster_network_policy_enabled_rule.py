from typing import Optional
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerClusterNetworkPolicy, GcpContainerClusterNetworkConfigProvider
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_network_policy_enabled_rule import ContainerClusterNetworkPolicyEnabledRule


class TestContainerClusterNetworkPolicyEnabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterNetworkPolicyEnabledRule()

    @parameterized.expand(
        [
            ["no_network_config", None, 1, RuleResultType.FAILED],
            ["network_config_not_enabled", GcpContainerClusterNetworkPolicy(GcpContainerClusterNetworkConfigProvider.CALICO, False), 1, RuleResultType.FAILED],
            ["network_config_enabled", GcpContainerClusterNetworkPolicy(GcpContainerClusterNetworkConfigProvider.CALICO, True), 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_network_config_enabled(self, unused_name: str,
                                                      network_config: Optional[GcpContainerClusterNetworkPolicy], total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        container_cluster.network_policy = network_config
        context = GcpEnvironmentContext(container_clusters=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
