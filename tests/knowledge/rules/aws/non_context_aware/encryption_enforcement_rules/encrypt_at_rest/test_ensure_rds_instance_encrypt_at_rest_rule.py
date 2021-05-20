import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.rds.rds_global_cluster import RdsGlobalCluster
from cloudrail.knowledge.context.aws.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_rds_instance_encrypt_at_rest_rule import \
    RdsEncryptAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestRdsEncryptAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = RdsEncryptAtRestRule()

    def test_not_car_rds_instances_encrypted_at_rest_fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        terraform_state = create_empty_entity(TerraformState)
        rds_instance.terraform_state = terraform_state
        rds_instance.terraform_state.is_new = True
        rds_instance.encrypted_at_rest = False
        context = EnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_rds_instances_encrypted_at_rest_pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        terraform_state = create_empty_entity(TerraformState)
        rds_instance.terraform_state = terraform_state
        rds_instance.terraform_state.is_new = True
        rds_instance.encrypted_at_rest = True
        context = EnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_rds_instances_encrypted_at_rest__not_new__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        terraform_state = create_empty_entity(TerraformState)
        rds_instance.terraform_state = terraform_state
        rds_instance.terraform_state.is_new = False
        rds_instance.encrypted_at_rest = False
        context = EnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_rds_clusters_encrypted_at_rest_fail(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        terraform_state = create_empty_entity(TerraformState)
        rds_cluster.terraform_state = terraform_state
        rds_cluster.terraform_state.is_new = True
        rds_cluster.encrypted_at_rest = False
        context = EnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_rds_clusters_encrypted_at_rest_pass(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        terraform_state = create_empty_entity(TerraformState)
        rds_cluster.terraform_state = terraform_state
        rds_cluster.terraform_state.is_new = True
        rds_cluster.encrypted_at_rest = True
        context = EnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_rds_clusters_encrypted_at_rest__not_new__pass(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        terraform_state = create_empty_entity(TerraformState)
        rds_cluster.terraform_state = terraform_state
        rds_cluster.terraform_state.is_new = False
        rds_cluster.encrypted_at_rest = False
        context = EnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_rds_global_cluster_encrypted_at_rest_fail(self):
        # Arrange
        rds_global_cluster: RdsGlobalCluster = create_empty_entity(RdsGlobalCluster)
        terraform_state = create_empty_entity(TerraformState)
        rds_global_cluster.terraform_state = terraform_state
        rds_global_cluster.terraform_state.is_new = True
        rds_global_cluster.encrypted_at_rest = False
        context = EnvironmentContext(rds_global_clusters=[rds_global_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_rds_global_cluster_encrypted_at_rest_pass(self):
        # Arrange
        rds_global_cluster: RdsGlobalCluster = create_empty_entity(RdsGlobalCluster)
        terraform_state = create_empty_entity(TerraformState)
        rds_global_cluster.terraform_state = terraform_state
        rds_global_cluster.terraform_state.is_new = True
        rds_global_cluster.encrypted_at_rest = True
        context = EnvironmentContext(rds_global_clusters=[rds_global_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_rds_global_cluster_encrypted_at_rest__not_new__pass(self):
        # Arrange
        rds_global_cluster: RdsGlobalCluster = create_empty_entity(RdsGlobalCluster)
        terraform_state = create_empty_entity(TerraformState)
        rds_global_cluster.terraform_state = terraform_state
        rds_global_cluster.terraform_state.is_new = False
        rds_global_cluster.encrypted_at_rest = False
        context = EnvironmentContext(rds_global_clusters=[rds_global_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
