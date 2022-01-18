from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_auth_client_cert_disabled_rule import ContainerClusterAuthClientCertDisabledRule


class TestContainerClusterAuthClientCertDisabledRule(TestCase):
    def setUp(self):
        self.rule = ContainerClusterAuthClientCertDisabledRule()

    @parameterized.expand(
        [
            ["cert_enabled", True, 1, RuleResultType.FAILED],
            ["cert_disabled", False, 0, RuleResultType.SUCCESS],
        ]
    )

    def test_container_cluster_auth_client_cert(self, unused_name: str,
                                                      issue_client_certificate: bool,
                                                      total_issues: int, rule_status: RuleResultType):
        # Arrange
        container_cluster = create_empty_entity(GcpContainerCluster)
        container_cluster.issue_client_certificate = issue_client_certificate
        context = GcpEnvironmentContext(container_cluster=[container_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
