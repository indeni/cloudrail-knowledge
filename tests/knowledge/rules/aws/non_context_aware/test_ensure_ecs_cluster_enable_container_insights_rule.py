import unittest

from cloudrail.knowledge.context.aws.resources.ecs.ecs_cluster import EcsCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecs_cluster_enable_container_insights_rule import \
    EnsureEcsClusterEnableContainerInsightsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureEcsClusterEnableContainerInsightsRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEcsClusterEnableContainerInsightsRule()

    def test_non_car_ecs_cluster_container_insights_enabled_fail(self):
        # Arrange
        ecs_cluster: EcsCluster = create_empty_entity(EcsCluster)
        ecs_cluster.is_container_insights_enabled = False
        context = AwsEnvironmentContext(ecs_cluster_list=[ecs_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ecs_cluster_container_insights_enabled_pass(self):
        # Arrange
        ecs_cluster: EcsCluster = create_empty_entity(EcsCluster)
        ecs_cluster.is_container_insights_enabled = True
        context = AwsEnvironmentContext(ecs_cluster_list=[ecs_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
