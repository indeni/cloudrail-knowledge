from cloudrail.knowledge.rules.azure.non_context_aware.vpn_gateway_disallow_basic_sku_rule import VpnGatewayDisallowBasicSkuRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestVpnGatewayDisallowBasicSkuRule(AzureBaseRuleTest):
    def get_rule(self):
        return VpnGatewayDisallowBasicSkuRule()

    def test_vpn_gw_is_basic(self):
        self.run_test_case('vpn_gw_is_basic', should_alert=True)

    def test_vpn_gw_not_basic(self):
        self.run_test_case('vpn_gw_not_basic', should_alert=False)

    def test_non_vpn_gw_is_basic(self):
        self.run_test_case('non_vpn_gw_is_basic', should_alert=False)

    def test_non_vpn_gw_not_basic(self):
        self.run_test_case('non_vpn_gw_not_basic', should_alert=False)
