from typing import Optional
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerClusterPrivateClusterConfig
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_private_cluster_enabled_rule import ContainerClusterPrivateClusterEnabledRule


class TestContainerClusterPrivateClusterEnabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterPrivateClusterEnabledRule()

    @parameterized.expand(
        [
            ["no_cluster_config", False, None, 1, RuleResultType.FAILED],
            ["disabled", True, False, 1, RuleResultType.FAILED],
            ["enabled", True, True, 0, RuleResultType.SUCCESS]
        ]
    )

    def test_container_cluster_private_cluster_enabled_rule(self, unused_name: str, private_cluster_config: bool,
                                                            enable_private_endpoint: Optional[bool],
                                                            total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        if private_cluster_config:
            private_cluster: GcpContainerClusterPrivateClusterConfig = create_empty_entity(GcpContainerClusterPrivateClusterConfig)
            private_cluster.enable_private_endpoint = enable_private_endpoint
            container_cluster.private_cluster_config = private_cluster
        context = GcpEnvironmentContext(container_clusters=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
