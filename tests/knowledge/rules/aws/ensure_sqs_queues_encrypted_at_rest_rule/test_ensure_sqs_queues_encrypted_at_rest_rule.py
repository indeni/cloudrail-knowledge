from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sqs_queues_encrypted_at_rest_rule import \
    EnsureSqsQueuesEncryptedAtRestRule


class TestEnsureSqsQueuesEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSqsQueuesEncryptedAtRestRule()

    @rule_test('no_encryption', True)
    def test_no_encryption(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypted_at_rest', False)
    def test_encrypted_at_rest(self, rule_result: RuleResponse):
        pass
