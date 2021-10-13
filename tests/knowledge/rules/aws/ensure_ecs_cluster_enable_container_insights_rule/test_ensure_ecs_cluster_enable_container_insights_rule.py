from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecs_cluster_enable_container_insights_rule import \
    EnsureEcsClusterEnableContainerInsightsRule

from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEcsClusterEnableContainerInsightsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcsClusterEnableContainerInsightsRule()

    def test_ecs_disable_insight(self):
        self.run_test_case('ecs_disable_insight', True)

    def test_ecs_with_container_insights(self):
        self.run_test_case('ecs_with_container_insights', False)
