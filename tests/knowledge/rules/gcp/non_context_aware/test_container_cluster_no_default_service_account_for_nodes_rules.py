from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster_node_config import GcpContainerClusterNodeConfig
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_no_default_service_account_for_nodes_rules import \
    ContainerClusterNoDefaultServiceAccountForNodesRule


class TestContainerClusterNoDefaultServiceAccountForNodesRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterNoDefaultServiceAccountForNodesRule()

    @parameterized.expand(
        [
            ["default_service_account_used", 'default', 1, RuleResultType.FAILED],
            ["not_default_service_account", 'non-default-svc-001@dev-for-tests.iam.gserviceaccount.com', 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_no_default_service_account_usage(self, unused_name: str,
                                                                service_account: str,
                                                                total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        node_config: GcpContainerClusterNodeConfig = create_empty_entity(GcpContainerClusterNodeConfig)
        node_config.service_account = service_account
        container_cluster.node_config = node_config
        context = GcpEnvironmentContext(container_clusters=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
