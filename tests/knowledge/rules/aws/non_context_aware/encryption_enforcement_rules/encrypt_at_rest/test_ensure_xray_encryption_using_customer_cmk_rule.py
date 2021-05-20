import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.xray.xray_encryption import XrayEncryption
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_xray_encryption_using_customer_cmk_rule import EnsureXrayEncryptionCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureXrayEncryptionCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureXrayEncryptionCmkRule()

    def test_non_car_xray_encryption_config_encrypt_at_rest_with_customer_managed_CMK_fail(self):
        # Arrange
        xray_config: XrayEncryption = create_empty_entity(XrayEncryption)
        xray_config.key_id = True
        xray_config.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = EnvironmentContext(xray_encryption_configurations=[xray_config])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_xray_encryption_config_encrypt_at_rest_with_customer_managed_CMK__key_id_false__fail(self):
        # Arrange
        xray_config: XrayEncryption = create_empty_entity(XrayEncryption)
        xray_config.key_id = True
        xray_config.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = EnvironmentContext(xray_encryption_configurations=[xray_config])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_xray_encryption_config_encrypt_at_rest_with_customer_managed_CMK_pass(self):
        # Arrange
        xray_config: XrayEncryption = create_empty_entity(XrayEncryption)
        xray_config.key_id = True
        xray_config.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = EnvironmentContext(xray_encryption_configurations=[xray_config])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
