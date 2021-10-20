from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.vpn_gateway_disallow_basic_sku_rule import VpnGatewayDisallowBasicSkuRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestVpnGatewayDisallowBasicSkuRule(AzureBaseRuleTest):
    def get_rule(self):
        return VpnGatewayDisallowBasicSkuRule()

    @rule_test('vpn_gw_is_basic', should_alert=True)
    def test_vpn_gw_is_basic(self, rule_result: RuleResponse):
        pass

    @rule_test('vpn_gw_not_basic', should_alert=False)
    def test_vpn_gw_not_basic(self, rule_result: RuleResponse):
        pass

    @rule_test('non_vpn_gw_is_basic', should_alert=False)
    def test_non_vpn_gw_is_basic(self, rule_result: RuleResponse):
        pass

    @rule_test('non_vpn_gw_not_basic', should_alert=False)
    def test_non_vpn_gw_not_basic(self, rule_result: RuleResponse):
        pass
