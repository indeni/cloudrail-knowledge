from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerClusterNetworkingMode
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_alias_ip_used_rule import ContainerClusterAliasIPUsedRule


class TestContainerClusterAliasIPUsedRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterAliasIPUsedRule()

    @parameterized.expand(
        [
            ["no_alias_ip_used", GcpContainerClusterNetworkingMode.ROUTES, 1, RuleResultType.FAILED],
            ["alias_ip_used", GcpContainerClusterNetworkingMode.VPC_NATIVE, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_alias_ip_used(self, unused_name: str, networking_mode: GcpContainerClusterNetworkingMode, total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        container_cluster.networking_mode = networking_mode
        context = GcpEnvironmentContext(container_cluster=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
