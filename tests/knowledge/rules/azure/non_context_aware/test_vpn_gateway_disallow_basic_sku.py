import unittest

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.non_context_aware.vpn_gateway_disallow_basic_sku_rule import VpnGatewayDisallowBasicSkuRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.network.azure_vnet_gateway import AzureVirtualNetworkGateway, VirtualNetworkGatewayType


class TestVpnGatewayDisallowBasicSku(unittest.TestCase):
    def setUp(self):
        self.rule = VpnGatewayDisallowBasicSkuRule()

    @parameterized.expand([
        ['Basic VPN - Should Alert', VirtualNetworkGatewayType.VPN, 'Basic', True],
        ['Basic Express Route - Ok', VirtualNetworkGatewayType.EXPRESS_ROUTE, 'Basic', False],
        ['Standard VPN - Ok', VirtualNetworkGatewayType.VPN, 'Standard', False],
    ])
    def test_vpn_gateway_disallow_basic_sku(self, unused_name: str, gw_type: VirtualNetworkGatewayType, sku: str, should_alert: bool):
        # Arrange
        vpn_gw = create_empty_entity(AzureVirtualNetworkGateway)
        vpn_gw.gateway_type = gw_type
        vpn_gw.sku_tier = sku
        context = AzureEnvironmentContext(vnet_gateways=AliasesDict(vpn_gw))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
