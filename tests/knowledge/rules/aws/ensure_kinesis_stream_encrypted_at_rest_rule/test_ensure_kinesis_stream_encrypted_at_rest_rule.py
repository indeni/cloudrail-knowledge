from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_kinesis_stream_encrypted_at_rest_rule import \
    EnsureKinesisStreamEncryptedAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest

class TestEnsureKinesisStreamEncryptedAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureKinesisStreamEncryptedAtRestRule()

    def test_encrypted_at_rest(self):
        self.run_test_case('encrypted_at_rest', False)

    def test_not_encrypted_at_rest(self):
        self.run_test_case('not_encrypted_at_rest', True, 2)
