from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_kinesis_firehose_stream_encypted_at_rest_rule import \
    EnsureKinesisFirehoseStreamEncryptedAtRestRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureKinesisFirehoseStreamEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureKinesisFirehoseStreamEncryptedAtRestRule()

    def test_encrypted_at_rest(self):
        self.run_test_case('encrypted_at_rest', False)

    def test_not_encrypted(self):
        self.run_test_case('not_encrypted', True)
