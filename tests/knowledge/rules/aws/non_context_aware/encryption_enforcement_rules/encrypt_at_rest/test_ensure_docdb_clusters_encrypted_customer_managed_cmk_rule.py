import unittest

from cloudrail.knowledge.context.aws.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_docdb_clusters_encrypted_customer_managed_cmk_rule import \
    EnsureDocdbClustersEncryptedCustomerManagedCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureDocdbClustersEncryptedCustomerManagedCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureDocdbClustersEncryptedCustomerManagedCmkRule()

    def test_not_car_docdb_cluster_encrypted_at_rest_using_customer_managed_cmk__kms_key_is_not_customer__fail(self):
        # Arrange
        document_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        terraform_state = create_empty_entity(TerraformState)
        document_db_cluster.terraform_state = terraform_state
        document_db_cluster.terraform_state.is_new = True
        document_db_cluster.storage_encrypted = True
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.AWS
        document_db_cluster.kms_data = kms_key

        context = AwsEnvironmentContext(docdb_cluster=[document_db_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest_using_customer_managed_cmk__kms_key_is_missing__fail(self):
        # Arrange
        document_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        terraform_state = create_empty_entity(TerraformState)
        document_db_cluster.terraform_state = terraform_state
        document_db_cluster.terraform_state.is_new = True
        document_db_cluster.storage_encrypted = True
        document_db_cluster.kms_data = None

        context = AwsEnvironmentContext(docdb_cluster=[document_db_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest_using_customer_managed_cmk_pass(self):
        # Arrange
        document_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        terraform_state = create_empty_entity(TerraformState)
        document_db_cluster.terraform_state = terraform_state
        document_db_cluster.terraform_state.is_new = True
        document_db_cluster.storage_encrypted = True
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.CUSTOMER
        document_db_cluster.kms_data = kms_key

        context = AwsEnvironmentContext(docdb_cluster=[document_db_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
