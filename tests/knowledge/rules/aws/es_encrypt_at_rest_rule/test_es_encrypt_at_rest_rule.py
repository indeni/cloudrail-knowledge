from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.es_encrypt_at_rest_rule import EsEncryptAtRestRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEsEncryptAtRestRule(AwsBaseRuleTest):

    def get_rule(self):
        return EsEncryptAtRestRule()

    @rule_test('encrypt_at_rest_disabled', True)
    def test_encrypt_at_rest_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypt_at_rest_enabled', False)
    def test_encrypt_at_rest_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypt_at_rest_disabled_unsupported_ver', False)
    def test_encrypt_at_rest_disabled_unsupported_ver(self, rule_result: RuleResponse):
        pass
