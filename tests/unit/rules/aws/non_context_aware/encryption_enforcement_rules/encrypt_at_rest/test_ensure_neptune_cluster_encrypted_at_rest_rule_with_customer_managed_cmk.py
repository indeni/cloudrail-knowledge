import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.resources.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_neptune_cluster_encrypted_at_rest_rule_with_customer_managed_cmk import \
    EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule()

    def test_non_car_neptune_cluster_encrypt_at_rest_with_customer_managed_cmk_fail(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        terraform_state = create_empty_entity(IacState)
        neptune_cluster.iac_state = terraform_state
        neptune_cluster.iac_state.is_new = True
        neptune_cluster.encrypted_at_rest = True
        neptune_cluster.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_neptune_cluster_encrypt_at_rest_with_customer_managed_cmk_pass(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        terraform_state = create_empty_entity(IacState)
        neptune_cluster.iac_state = terraform_state
        neptune_cluster.iac_state.is_new = True
        neptune_cluster.encrypted_at_rest = True
        neptune_cluster.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_neptune_cluster_encrypt_at_rest_with_customer_managed__not_new_resource__cmk_pass(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        terraform_state = create_empty_entity(IacState)
        neptune_cluster.iac_state = terraform_state
        neptune_cluster.iac_state.is_new = False
        neptune_cluster.encrypted_at_rest = True
        neptune_cluster.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_neptune_cluster_encrypt_at_rest_with_customer_managed__no_kms_data__cmk_fail(self):
        # Arrange
        neptune_cluster: NeptuneCluster = create_empty_entity(NeptuneCluster)
        terraform_state = create_empty_entity(IacState)
        neptune_cluster.iac_state = terraform_state
        neptune_cluster.iac_state.is_new = True
        neptune_cluster.encrypted_at_rest = True
        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
