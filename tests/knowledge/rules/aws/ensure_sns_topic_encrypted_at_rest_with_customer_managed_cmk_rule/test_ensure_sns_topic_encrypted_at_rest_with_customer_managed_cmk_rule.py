from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.\
    ensure_sns_topic_encrypted_at_rest_with_customer_managed_cmk_rule import \
    EnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule()

    def test_encrypted_at_rest_with_aws_managed_key_by_key_arn(self):
        self.run_test_case('encrypted_at_rest_with_aws_managed_key_by_key_arn', True)

    def test_encrypted_at_rest_with_customer_managed_key_creating_key(self):
        self.run_test_case('encrypted_at_rest_with_customer_managed_key_creating_key', False)

    def test_encrypted_at_rest_with_customer_managed_key_existing_key(self):
        self.run_test_case('encrypted_at_rest_with_customer_managed_key_existing_key', False)
