import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.\
    encryption_enforcement_rules.encrypt_at_rest.ensure_neptune_cluster_encrypted_at_rest_rule import EnsureNeptuneClusterEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureNeptuneClusterEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureNeptuneClusterEncryptedAtRestRule()

    def test_non_car_neptune_cluster_encrypt_at_rest_creating_fail(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        terraform_state = create_empty_entity(TerraformState)
        neptune_cluster.terraform_state = terraform_state
        neptune_cluster.terraform_state.is_new = True
        neptune_cluster.encrypted_at_rest = False
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_neptune_cluster_encrypt_at_rest_creating_pass(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        terraform_state = create_empty_entity(TerraformState)
        neptune_cluster.terraform_state = terraform_state
        neptune_cluster.terraform_state.is_new = True
        neptune_cluster.encrypted_at_rest = True
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_neptune_cluster_encrypt_at_rest_creating__not_new__pass(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        terraform_state = create_empty_entity(TerraformState)
        neptune_cluster.terraform_state = terraform_state
        neptune_cluster.terraform_state.is_new = False
        neptune_cluster.encrypted_at_rest = False
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
