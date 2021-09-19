from cloudrail.knowledge.rules.azure.non_context_aware.kubernetes_cluster_rbac_enabled_rule import KubernetesClusterRbacEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestKubernetesClusterRbacEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return KubernetesClusterRbacEnabledRule()

    def test_kubernetes_rbac_enabled(self):
        self.run_test_case('kubernetes_rbac_enabled', False)

    def test_kubernetes_rbac_disabled(self):
        self.run_test_case('kubernetes_rbac_disabled', True)
