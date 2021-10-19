from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_sagemaker_endpoint_config_encrypted_at_rest_rule import \
    EnsureSageMakerEndpointConfigEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureSageMakerEndpointConfigEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSageMakerEndpointConfigEncryptedAtRestRule()

    @rule_test('sagemaker_endpoint_config_encrypted', False)
    def test_sagemaker_endpoint_config_encrypted(self, rule_result: RuleResponse):
        pass

    @rule_test('sagemaker_endpoint_config_non_encrypted', True)
    def test_sagemaker_endpoint_config_non_encrypted(self, rule_result: RuleResponse):
        pass
