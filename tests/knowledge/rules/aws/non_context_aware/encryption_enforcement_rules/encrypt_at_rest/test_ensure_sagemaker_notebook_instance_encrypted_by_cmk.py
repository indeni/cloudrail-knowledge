import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.sagemaker.sagemaker_notebook_instance import SageMakerNotebookInstance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_sagemaker_notebook_instance_encrypted_by_cmk import EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule()

    def test_not_car_sagemaker_notebook_instances_encrypt_artifacts_at_rest_with_customer_managed_CMK_creating_fail(self):
        # Arrange
        sagemaker_instance: SageMakerNotebookInstance = create_empty_entity(SageMakerNotebookInstance)
        terraform_state = create_empty_entity(TerraformState)
        sagemaker_instance.terraform_state = terraform_state
        sagemaker_instance.terraform_state.is_new = True
        sagemaker_instance.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(sagemaker_notebook_instances=[sagemaker_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_sagemaker_notebook_instances_encrypt_artifacts_at_rest_with_customer_managed_CMK_creating_pass(self):
        # Arrange
        sagemaker_instance: SageMakerNotebookInstance = create_empty_entity(SageMakerNotebookInstance)
        terraform_state = create_empty_entity(TerraformState)
        sagemaker_instance.terraform_state = terraform_state
        sagemaker_instance.terraform_state.is_new = True
        sagemaker_instance.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(sagemaker_notebook_instances=[sagemaker_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_sagemaker_notebook_instances_encrypt_artifacts_at_rest_with_customer_managed_CMK_creating__not_new__pass(self):
        # Arrange
        sagemaker_instance: SageMakerNotebookInstance = create_empty_entity(SageMakerNotebookInstance)
        terraform_state = create_empty_entity(TerraformState)
        sagemaker_instance.terraform_state = terraform_state
        sagemaker_instance.terraform_state.is_new = False
        sagemaker_instance.kms_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = AwsEnvironmentContext(sagemaker_notebook_instances=[sagemaker_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
