import unittest

from cloudrail.knowledge.context.aws.ecr.ecr_repository import EcrRepository
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_ecr_repositories_encrypt_at_rest_with_customer_cmk_rule import \
    EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule()

    def test_not_car_docdb_cluster_encrypted_at_rest__repo_no_kms_encrypt__fail(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        terraform_state = create_empty_entity(TerraformState)
        ecr_repo.terraform_state = terraform_state
        ecr_repo.terraform_state.is_new = True
        ecr_repo.encryption_type = 'AES256'

        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest__encrypt_AWS_keys__fail(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        terraform_state = create_empty_entity(TerraformState)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.AWS
        ecr_repo.terraform_state = terraform_state
        ecr_repo.terraform_state.is_new = True
        ecr_repo.encryption_type = 'KMS'
        ecr_repo.kms_data = kms_key

        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest__encrypt_AWS_keys_not_new_resource__pass(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        terraform_state = create_empty_entity(TerraformState)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.AWS
        ecr_repo.terraform_state = terraform_state
        ecr_repo.terraform_state.is_new = False
        ecr_repo.encryption_type = 'KMS'
        ecr_repo.kms_data = kms_key

        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest__encrypt_customer_keys__pass(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        terraform_state = create_empty_entity(TerraformState)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.CUSTOMER
        ecr_repo.terraform_state = terraform_state
        ecr_repo.terraform_state.is_new = True
        ecr_repo.encryption_type = 'KMS'
        ecr_repo.kms_data = kms_key

        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
