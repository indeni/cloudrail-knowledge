import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.sagemaker.sagemaker_endpoint_config import SageMakerEndpointConfig
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_sagemaker_endpoint_config_encrypted_at_rest_rule import EnsureSageMakerEndpointConfigEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureSageMakerEndpointConfigEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSageMakerEndpointConfigEncryptedAtRestRule()

    def test_not_car_sagemaker_endpoint_configurations_encrypt_data_at_rest_fail(self):
        # Arrange
        sagemaker_endpoint: SageMakerEndpointConfig = create_empty_entity(SageMakerEndpointConfig)
        terraform_state = create_empty_entity(IacState)
        sagemaker_endpoint.iac_state = terraform_state
        sagemaker_endpoint.iac_state.is_new = True
        sagemaker_endpoint.encrypted = False
        context = AwsEnvironmentContext(sagemaker_endpoint_config_list=[sagemaker_endpoint])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_sagemaker_endpoint_configurations_encrypt_data_at_rest_pass(self):
        # Arrange
        sagemaker_endpoint: SageMakerEndpointConfig = create_empty_entity(SageMakerEndpointConfig)
        terraform_state = create_empty_entity(IacState)
        sagemaker_endpoint.iac_state = terraform_state
        sagemaker_endpoint.iac_state.is_new = True
        sagemaker_endpoint.encrypted = True
        context = AwsEnvironmentContext(sagemaker_endpoint_config_list=[sagemaker_endpoint])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_sagemaker_endpoint_configurations_encrypt_data_at_rest__not_new__pass(self):
        # Arrange
        sagemaker_endpoint: SageMakerEndpointConfig = create_empty_entity(SageMakerEndpointConfig)
        terraform_state = create_empty_entity(IacState)
        sagemaker_endpoint.iac_state = terraform_state
        sagemaker_endpoint.iac_state.is_new = False
        sagemaker_endpoint.encrypted = False
        context = AwsEnvironmentContext(sagemaker_endpoint_config_list=[sagemaker_endpoint])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
