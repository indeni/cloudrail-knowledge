from typing import List
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerMasterAuthNetConfig, GcpContainerMasterAuthNetConfigCidrBlk
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_is_not_public_rule import ContainerClusterIsNotPublictRule


class TestContainerClusterIsNotPublictRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterIsNotPublictRule()

    @parameterized.expand(
        [
            ["One cluster is public", ["10.0.0.0/8", ""], 1, RuleResultType.FAILED],
            ["Both clusters are public", ["", ""], 2, RuleResultType.FAILED],
            ["Both clusters are private", ["10.0.0.0/8", "10.0.0.0/8"], 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_is_not_public(self, unused_name: str, cidr_blocks: List[str], total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_clusters: List[GcpContainerCluster] = []
        for cidr_block in cidr_blocks:
            container_cluster = create_empty_entity(GcpContainerCluster)
            if cidr_block:
                container_cluster.master_authorized_networks_config = create_empty_entity(GcpContainerMasterAuthNetConfig)
                container_cluster.master_authorized_networks_config.cidr_blocks = [create_empty_entity(GcpContainerMasterAuthNetConfigCidrBlk)]
                container_cluster.master_authorized_networks_config.cidr_blocks[0].cidr_block = cidr_block
            container_clusters.append(container_cluster)

        context = GcpEnvironmentContext(container_cluster=container_clusters)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
