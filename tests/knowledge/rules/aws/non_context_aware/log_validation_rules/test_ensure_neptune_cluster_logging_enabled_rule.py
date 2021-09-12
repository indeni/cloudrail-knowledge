import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_neptune_cluster_logging_enabled_rule import \
    EnsureNeptuneClusterLoggingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureNeptuneClusterLoggingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureNeptuneClusterLoggingEnabledRule()

    def test_non_car_neptune_cluster_logging_enabled__no_logs_at_all__fail(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_neptune_cluster_logging_enabled__no_audit_logs__fail(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        neptune_cluster.cloudwatch_logs_exports = ['trace']
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_neptune_cluster_logging_enabled_pass(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        neptune_cluster.cloudwatch_logs_exports = ['audit']
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
