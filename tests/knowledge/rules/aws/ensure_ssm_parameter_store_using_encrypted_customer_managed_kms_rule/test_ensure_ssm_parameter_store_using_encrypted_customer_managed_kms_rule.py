from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_ssm_parameter_store_using_encrypted_customer_managed_kms_rule import \
    EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule()

    @rule_test('default_encryption', True)
    def test_default_encryption(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_aws_managed_key_arn', True)
    def test_encrypted_aws_managed_key_arn(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_customer_kms_creating', False)
    def test_encrypted_customer_kms_creating(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_customer_kms_existing_key', False)
    def test_encrypted_customer_kms_existing_key(self, rule_result: RuleResponse):
        pass
