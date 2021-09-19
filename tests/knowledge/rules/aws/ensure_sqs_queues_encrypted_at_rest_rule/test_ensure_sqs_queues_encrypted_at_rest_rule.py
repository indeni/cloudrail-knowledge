from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sqs_queues_encrypted_at_rest_rule import \
    EnsureSqsQueuesEncryptedAtRestRule


class TestEnsureSqsQueuesEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSqsQueuesEncryptedAtRestRule()

    def test_no_encryption(self):
        self.run_test_case('no_encryption', True)

    def test_encrypted_at_rest(self):
        self.run_test_case('encrypted_at_rest', False)
