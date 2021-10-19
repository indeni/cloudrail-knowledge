from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_kinesis_firehose_stream_encypted_at_rest_rule import \
    EnsureKinesisFirehoseStreamEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureKinesisFirehoseStreamEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureKinesisFirehoseStreamEncryptedAtRestRule()

    @rule_test('encrypted_at_rest', False)
    def test_encrypted_at_rest(self, rule_result: RuleResponse):
        pass

    @rule_test('not_encrypted', True)
    def test_not_encrypted(self, rule_result: RuleResponse):
        pass
