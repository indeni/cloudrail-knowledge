import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.ssm.ssm_parameter import SsmParameter
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_ssm_parameter_store_using_encrypted_customer_managed_kms_rule import\
    EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule()

    def test_non_car_ssm_parameter_store_securestring_encrypted_at_rest_with_customer_managed_CMK_fail(self):
        # Arrange
        ssm_param: SsmParameter = create_empty_entity(SsmParameter)
        ssm_param.name = 'ssm_test'
        ssm_param.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = EnvironmentContext(ssm_parameters=[ssm_param])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ssm_parameter_store_securestring_encrypted_at_rest_with_customer_managed_CMK__no_kms_data__fail(self):
        # Arrange
        ssm_param: SsmParameter = create_empty_entity(SsmParameter)
        ssm_param.name = 'ssm_test'
        ssm_param.kms_data = None
        context = EnvironmentContext(ssm_parameters=[ssm_param])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ssm_parameter_store_securestring_encrypted_at_rest_with_customer_managed_CMK_pass(self):
        # Arrange
        ssm_param: SsmParameter = create_empty_entity(SsmParameter)
        ssm_param.name = 'ssm_test'
        ssm_param.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = EnvironmentContext(ssm_parameters=[ssm_param])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
