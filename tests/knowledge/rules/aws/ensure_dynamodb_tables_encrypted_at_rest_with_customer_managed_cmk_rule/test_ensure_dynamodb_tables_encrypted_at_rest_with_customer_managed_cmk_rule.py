from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_dynamodb_tables_encrypted_at_rest_with_customer_managed_cmk_rule import \
    EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule()

    @rule_test('encrypted_customer_managed_new_key', False)
    def test_encrypted_customer_managed_new_key(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_default_aws_managed', True)
    def test_encrypted_default_aws_managed(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_default_aws_by_key_arn', True)
    def test_encrypted_default_aws_by_key_arn(self, rule_result: RuleResponse):
        pass

    @rule_test('no_encryption_at_all', True)
    def test_no_encryption_at_all(self, rule_result: RuleResponse):
        pass
