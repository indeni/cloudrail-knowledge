from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.kubernetes_cluster_rbac_enabled_rule import KubernetesClusterRbacEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestKubernetesClusterRbacEnabledRule(AzureBaseRuleTest):
    def get_rule(self):
        return KubernetesClusterRbacEnabledRule()

    @rule_test('kubernetes_rbac_enabled', False)
    def test_kubernetes_rbac_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('kubernetes_rbac_disabled', True)
    def test_kubernetes_rbac_disabled(self, rule_result: RuleResponse):
        pass
