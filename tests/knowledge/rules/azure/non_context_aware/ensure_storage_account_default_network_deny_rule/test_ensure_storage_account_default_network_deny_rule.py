from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_storage_account_default_network_deny_rule import EnsureStorageAccountDefaultNetworkDenyRule


class TestEnsureStorageAccountDefaultNetworkDenyRule(AzureBaseRuleTest):

    def get_rule(self):
        return EnsureStorageAccountDefaultNetworkDenyRule()

    @rule_test('default_network_access_allow_internal_block', True)
    def test_default_network_access_allow_internal_block(self, rule_result: RuleResponse):
        pass

    @rule_test('default_network_access_allow_no_block', True)
    def test_default_network_access_allow_no_block(self, rule_result: RuleResponse):
        pass

    @rule_test('default_network_access_deny_internal_block', False)
    def test_default_network_access_deny_internal_block(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_network_rules_allow', True)
    def test_storage_network_rules_allow(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_network_rules_deny', False)
    def test_storage_network_rules_deny(self, rule_result: RuleResponse):
        pass
