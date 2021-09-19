import unittest

from cloudrail.knowledge.context.aws.resources.dax.dax_cluster import DaxCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_dax_clusters_encrypted_rule import \
    EnsureDaxClustersEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureDaxClustersEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureDaxClustersEncryptedRule()

    def test_not_car_dynamodb_dax_clusters_encrypted_at_rest_fail(self):
        # Arrange
        dax_cluster: DaxCluster = create_empty_entity(DaxCluster)
        terraform_state = create_empty_entity(IacState)
        dax_cluster.iac_state = terraform_state
        dax_cluster.iac_state.is_new = True
        dax_cluster.server_side_encryption = False

        context = AwsEnvironmentContext(dax_cluster=[dax_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_dynamodb_dax_clusters_encrypted_at_rest__not_new_resource__pass(self):
        # Arrange
        dax_cluster: DaxCluster = create_empty_entity(DaxCluster)
        terraform_state = create_empty_entity(IacState)
        dax_cluster.iac_state = terraform_state
        dax_cluster.iac_state.is_new = False
        dax_cluster.server_side_encryption = True

        context = AwsEnvironmentContext(dax_cluster=[dax_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_dynamodb_dax_clusters_encrypted_at_rest__new_resource__pass(self):
        # Arrange
        dax_cluster: DaxCluster = create_empty_entity(DaxCluster)
        terraform_state = create_empty_entity(IacState)
        dax_cluster.iac_state = terraform_state
        dax_cluster.iac_state.is_new = True
        dax_cluster.server_side_encryption = True

        context = AwsEnvironmentContext(dax_cluster=[dax_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
