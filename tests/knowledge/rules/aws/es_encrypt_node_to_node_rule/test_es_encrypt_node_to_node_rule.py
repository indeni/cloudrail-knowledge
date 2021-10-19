from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.es_encrypt_node_to_node_rule import EsEncryptNodeToNodeRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEsEncryptNodeToNodeRule(AwsBaseRuleTest):

    def get_rule(self):
        return EsEncryptNodeToNodeRule()

    @rule_test('encrypt_node_to_node_disabled', True)
    def test_encrypt_node_to_node_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypt_node_to_node_enabled', False)
    def test_encrypt_node_to_node_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('encrypt_node_to_node_disabled_unsupported_version', False)
    def test_encrypt_node_to_node_disabled_unsupported_version(self, rule_result: RuleResponse):
        pass
