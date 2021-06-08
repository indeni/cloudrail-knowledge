import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_redshift_cluster_created_encrypted_rule import EnsureRedshiftClusterCreatedEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRedshiftClusterCreatedEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRedshiftClusterCreatedEncryptedRule()

    def test_non_car_redshift_cluster_encrypt_at_rest_creating_fail(self):
        # Arrange
        redshift_cluster: RedshiftCluster = create_empty_entity(RedshiftCluster)
        terraform_state = create_empty_entity(TerraformState)
        redshift_cluster.terraform_state = terraform_state
        redshift_cluster.terraform_state.is_new = True
        redshift_cluster.encrypted = False
        context = AwsEnvironmentContext(redshift_clusters=[redshift_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_redshift_cluster_encrypt_at_rest_creating_pass(self):
        # Arrange
        redshift_cluster: RedshiftCluster = create_empty_entity(RedshiftCluster)
        terraform_state = create_empty_entity(TerraformState)
        redshift_cluster.terraform_state = terraform_state
        redshift_cluster.terraform_state.is_new = True
        redshift_cluster.encrypted = True
        context = AwsEnvironmentContext(redshift_clusters=[redshift_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_redshift_cluster_encrypt_at_rest_creating__not_new__pass(self):
        # Arrange
        redshift_cluster: RedshiftCluster = create_empty_entity(RedshiftCluster)
        terraform_state = create_empty_entity(TerraformState)
        redshift_cluster.terraform_state = terraform_state
        redshift_cluster.terraform_state.is_new = False
        redshift_cluster.encrypted = False
        context = AwsEnvironmentContext(redshift_clusters=[redshift_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
