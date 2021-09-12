import unittest

from cloudrail.knowledge.context.azure.resources.aks.azure_kubernetes_cluster import AzureKubernetesCluster
from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.non_context_aware.kubernetes_cluster_rbac_enabled_rule import KubernetesClusterRbacEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestKubernetesClusterRbacEnabled(unittest.TestCase):

    def setUp(self):
        self.rule = KubernetesClusterRbacEnabledRule()

    @parameterized.expand(
        [
            ['RBAC Enabled', True, False],
            ['RBAC Disabled', False, True],
        ]
    )
    def test_rbac(self, unused_name: str, enable_rbac: bool, should_alert: bool):
        # Arrange
        kubernetes_cluster: AzureKubernetesCluster = create_empty_entity(AzureKubernetesCluster)
        kubernetes_cluster.name = 'tmp-name'
        kubernetes_cluster.enable_rbac = enable_rbac

        context = AzureEnvironmentContext(kubernetes_cluster=AliasesDict(kubernetes_cluster))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
