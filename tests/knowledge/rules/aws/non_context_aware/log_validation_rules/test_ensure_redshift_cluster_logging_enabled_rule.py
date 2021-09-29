import unittest

from cloudrail.knowledge.context.aws.resources.redshift.redshift_logging import RedshiftLogging

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_redshift_cluster_logging_enabled_rule import \
    EnsureRedshiftClusterLoggingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRedshiftClusterLoggingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRedshiftClusterLoggingEnabledRule()

    def test_non_car_redshift_cluster_logging_enabled__no_logs_field__fail(self):
        # Arrange
        redshift_cluster: RedshiftCluster = create_empty_entity(RedshiftCluster)
        context = AwsEnvironmentContext(redshift_clusters=[redshift_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_redshift_cluster_logging_enabled__logs_not_enabled__fail(self):
        # Arrange
        redshift_cluster: RedshiftCluster = create_empty_entity(RedshiftCluster)
        redshift_logs: RedshiftLogging = create_empty_entity(RedshiftLogging)
        redshift_logs.logging_enabled = False
        redshift_cluster.logs_config = redshift_logs
        context = AwsEnvironmentContext(redshift_clusters=[redshift_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_redshift_cluster_logging_enabled_pass(self):
        # Arrange
        redshift_cluster: RedshiftCluster = create_empty_entity(RedshiftCluster)
        redshift_logs: RedshiftLogging = create_empty_entity(RedshiftLogging)
        redshift_logs.logging_enabled = True
        redshift_cluster.logs_config = redshift_logs
        context = AwsEnvironmentContext(redshift_clusters=[redshift_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
