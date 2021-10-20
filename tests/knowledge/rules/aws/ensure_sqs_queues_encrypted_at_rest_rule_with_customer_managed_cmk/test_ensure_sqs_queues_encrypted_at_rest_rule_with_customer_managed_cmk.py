from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest\
    .ensure_sqs_queues_encrypted_at_rest_with_customer_managed_cmk_rule import \
    EnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test



class TestEnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule()

    @rule_test('encrypted_at_rest_with_aws_managed_key_by_key_arn', True)
    def test_encrypted_at_rest_with_aws_managed_key_by_key_arn(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_at_rest_with_customer_managed_key_creating_key', False,)
    def test_encrypted_at_rest_with_customer_managed_key_creating_key(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_at_rest_with_customer_managed_key_existing_key', False)
    def test_encrypted_at_rest_with_customer_managed_key_existing_key(self, rule_result: RuleResponse):
        pass
