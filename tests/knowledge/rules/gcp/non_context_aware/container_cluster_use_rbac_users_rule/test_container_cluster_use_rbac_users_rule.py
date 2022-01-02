from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.container_cluster_use_rbac_users_rule import ContainerClusterUseRbacUsersRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestContainerClusterUseRbacUsersRule(GcpBaseRuleTest):

    def get_rule(self):
        return ContainerClusterUseRbacUsersRule()

    @rule_test('cluster_with_optional', should_alert=False)
    def test_cluster_with_optional(self, rule_result: RuleResponse):
        pass

    @rule_test('cluster_without_optional', should_alert=True)
    def test_cluster_without_optional(self, rule_result: RuleResponse):
        pass
