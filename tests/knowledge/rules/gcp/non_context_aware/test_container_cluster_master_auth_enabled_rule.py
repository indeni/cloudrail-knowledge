from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerMasterAuthNetConfig, \
    GcpContainerMasterAuthNetConfigCidrBlk
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_master_auth_enabled_rule import ContainerClusterMasterAuthEnabledRule


class TestContainerClusterMasterAuthEnabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterMasterAuthEnabledRule()

    @parameterized.expand(
        [
            ["no_master_auth", False, 1, RuleResultType.FAILED],
            ["master_auth_enabled", True, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_master_auth_enabled(self, unused_name: str,
                                                   master_auth_enabled: bool,
                                                   total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        if master_auth_enabled:
            master_auth_config: GcpContainerMasterAuthNetConfig = create_empty_entity(GcpContainerMasterAuthNetConfig)
            cidr_block_config: GcpContainerMasterAuthNetConfigCidrBlk = create_empty_entity(GcpContainerMasterAuthNetConfigCidrBlk)
            cidr_block_config.cidr_block = '0.0.0.0/0'
            cidr_block_config.display_name = 'example'
            master_auth_config.cidr_blocks = cidr_block_config
            container_cluster.master_authorized_networks_config = master_auth_config
        context = GcpEnvironmentContext(container_cluster=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
