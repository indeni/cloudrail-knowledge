import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_rds_cluster_instances_encrypted_at_rest_rule_with_customer_managed_cmk import \
    EnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule()

    def test_non_car_rds_cluster_instance_encrypt_performance_insights_with_customer_managed_cmk_creating_fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        terraform_state = create_empty_entity(TerraformState)
        rds_instance.terraform_state = terraform_state
        rds_instance.terraform_state.is_new = True
        rds_instance.performance_insights_enabled = True
        rds_instance.performance_insights_kms_data = KmsKey(key_id='key', arn='arn',
                                                            key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_cluster_instance_encrypt_performance_insights_with_customer_managed_cmk_creating__no_kms_data__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        terraform_state = create_empty_entity(TerraformState)
        rds_instance.terraform_state = terraform_state
        rds_instance.terraform_state.is_new = True
        rds_instance.performance_insights_enabled = True
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_cluster_instance_encrypt_performance_insights_with_customer_managed_cmk_creating_pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        terraform_state = create_empty_entity(TerraformState)
        rds_instance.terraform_state = terraform_state
        rds_instance.terraform_state.is_new = True
        rds_instance.performance_insights_enabled = False
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_cluster_instance_encrypt_performance_insights_with_customer_managed_cmk_creating__key_manager_customer__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        terraform_state = create_empty_entity(TerraformState)
        rds_instance.terraform_state = terraform_state
        rds_instance.terraform_state.is_new = True
        rds_instance.performance_insights_enabled = True
        rds_instance.performance_insights_kms_data = KmsKey(key_id='key', arn='arn',
                                                            key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_cluster_instance_encrypt_performance_insights_with_customer_managed_cmk_creating__not_new__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        terraform_state = create_empty_entity(TerraformState)
        rds_instance.terraform_state = terraform_state
        rds_instance.terraform_state.is_new = False
        rds_instance.performance_insights_enabled = True
        rds_instance.performance_insights_kms_data = KmsKey(key_id='key', arn='arn',
                                                            key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
