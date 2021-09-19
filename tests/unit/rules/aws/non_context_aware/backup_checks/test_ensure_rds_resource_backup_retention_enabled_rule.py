import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.backup_checks.ensure_rds_resource_backup_retention_enabled_rule import \
    EnsureRdsResourceBackupRetentionEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRdsResourceBackupRetentionEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRdsResourceBackupRetentionEnabledRule()

    def test_non_car_rds_instance_and_cluster_backup_retention_policy_fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.backup_retention_period = 0
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_instance_and_cluster_backup_retention_policy_pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.backup_retention_period = 5
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_instance_and_cluster_backup_retention_policy__rds_cluster__fail(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        rds_cluster.backup_retention_period = 0
        context = AwsEnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_instance_and_cluster_backup_retention_policy__rds_cluster__pass(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        rds_cluster.backup_retention_period = 5
        context = AwsEnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
