from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_ecr_repositories_encrypt_at_rest_with_customer_cmk_rule import\
    EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule

from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule()

    @rule_test('default_encryption', True)
    def test_default_encryption(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_using_aws_key', True)
    def test_encrypted_using_aws_key(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_cmk_new_key', False)
    def test_encrypted_cmk_new_key(self, rule_result: RuleResponse):
        pass
