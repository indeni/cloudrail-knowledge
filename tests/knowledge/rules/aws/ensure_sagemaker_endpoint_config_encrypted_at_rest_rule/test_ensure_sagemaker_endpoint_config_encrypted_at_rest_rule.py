from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_sagemaker_endpoint_config_encrypted_at_rest_rule import \
    EnsureSageMakerEndpointConfigEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureSageMakerEndpointConfigEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSageMakerEndpointConfigEncryptedAtRestRule()

    def test_sagemaker_endpoint_config_encrypted(self):
        self.run_test_case('sagemaker_endpoint_config_encrypted', False)

    def test_sagemaker_endpoint_config_non_encrypted(self):
        self.run_test_case('sagemaker_endpoint_config_non_encrypted', True)
