from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.es_encrypt_at_rest_rule import EsEncryptAtRestRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEsEncryptAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EsEncryptAtRestRule()

    def test_encrypt_at_rest_disabled(self):
        self.run_test_case('encrypt_at_rest_disabled', True)

    def test_encrypt_at_rest_enabled(self):
        self.run_test_case('encrypt_at_rest_enabled', False)

    def test_encrypt_at_rest_disabled_unsupported_ver(self):
        self.run_test_case('encrypt_at_rest_disabled_unsupported_ver', False)
