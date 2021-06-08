import unittest

from cloudrail.knowledge.context.aws.dynamodb.dynamodb_table import DynamoDbTable
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_dynamodb_tables_encrypted_at_rest_with_customer_managed_cmk_rule import \
    EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule()

    def test_not_car_docdb_cluster_encrypted_at_rest__no_encryption_al_all__fail(self):
        # Arrange
        dynamodb_table: DynamoDbTable = create_empty_entity(DynamoDbTable)
        dynamodb_table.server_side_encryption = False

        context = AwsEnvironmentContext(dynamodb_table_list=[dynamodb_table])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest__no_customer_key__fail(self):
        # Arrange
        dynamodb_table: DynamoDbTable = create_empty_entity(DynamoDbTable)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.AWS
        dynamodb_table.server_side_encryption = True
        dynamodb_table.kms_data = kms_key

        context = AwsEnvironmentContext(dynamodb_table_list=[dynamodb_table])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest_pass(self):
        # Arrange
        dynamodb_table: DynamoDbTable = create_empty_entity(DynamoDbTable)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.CUSTOMER
        dynamodb_table.server_side_encryption = True
        dynamodb_table.kms_data = kms_key

        context = AwsEnvironmentContext(dynamodb_table_list=[dynamodb_table])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
