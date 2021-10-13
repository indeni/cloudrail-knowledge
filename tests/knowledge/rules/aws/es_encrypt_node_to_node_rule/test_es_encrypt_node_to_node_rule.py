from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.es_encrypt_node_to_node_rule import EsEncryptNodeToNodeRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEsEncryptNodeToNodeRule(AwsBaseRuleTest):

    def get_rule(self):
        return EsEncryptNodeToNodeRule()

    def test_encrypt_node_to_node_disabled(self):
        self.run_test_case('encrypt_node_to_node_disabled', True)

    def test_encrypt_node_to_node_enabled(self):
        self.run_test_case('encrypt_node_to_node_enabled', False)

    def test_encrypt_node_to_node_disabled_unsupported_version(self):
        self.run_test_case('encrypt_node_to_node_disabled_unsupported_version', False)
