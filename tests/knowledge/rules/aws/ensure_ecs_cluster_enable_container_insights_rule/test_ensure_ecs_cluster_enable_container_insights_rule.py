from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecs_cluster_enable_container_insights_rule import \
    EnsureEcsClusterEnableContainerInsightsRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureEcsClusterEnableContainerInsightsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcsClusterEnableContainerInsightsRule()

    @rule_test('ecs_disable_insight', True)
    def test_ecs_disable_insight(self, rule_result: RuleResponse):
        pass

    @rule_test('ecs_with_container_insights', False)
    def test_ecs_with_container_insights(self, rule_result: RuleResponse):
        pass
