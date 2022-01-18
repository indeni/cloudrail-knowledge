from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerClusterAuthGrpConfig
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_use_rbac_users_rule import ContainerClusterUseRbacUsersRule


class TestContainerClusterUseRbacUsersRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterUseRbacUsersRule()

    @parameterized.expand(
        [
            ["without_auth_config", False, True],
            ["with_auth_config", True, False]
        ]
    )

    def test_container_cluster_use_rbac_users_rule(self, unused_name: str, with_auth_config: bool, should_alert: bool):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        auth_config = create_empty_entity(GcpContainerClusterAuthGrpConfig) if with_auth_config else None
        container_cluster.authenticator_groups_config = auth_config
        context = GcpEnvironmentContext(container_clusters=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
