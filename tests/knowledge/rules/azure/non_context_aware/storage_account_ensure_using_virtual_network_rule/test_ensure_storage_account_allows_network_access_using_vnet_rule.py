from cloudrail.knowledge.rules.azure.non_context_aware.ensure_storage_account_allows_network_access_using_vnet_rule import EnsureStorageAccountAllowsNetworkAccessUsingVnetRule
from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestEnsureStorageAccountAllowsNetworkAccessUsingVnetRule(AzureBaseRuleTest):
    def get_rule(self):
        return EnsureStorageAccountAllowsNetworkAccessUsingVnetRule()

    @rule_test('ip_rules_only', should_alert=True)
    def test_ip_rules_only(self, rule_result: RuleResponse):
        pass

    @rule_test('virtual_network_subnet_ids_only', should_alert=False)
    def test_virtual_network_subnet_ids_only(self, rule_result: RuleResponse):
        pass
