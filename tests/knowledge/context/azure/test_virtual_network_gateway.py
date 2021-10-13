from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.network.azure_vnet_gateway import AzureVirtualNetworkGateway, VirtualNetworkGatewayType

from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context


class TestVirtualNetworkGateway(AzureContextTest):

    def get_component(self):
        return "virtual_network_gateway"

    @context(module_path="express_route_vnet_gw")
    def test_express_route_vnet_gw(self, ctx: AzureEnvironmentContext):
        vnet_gw = self._get_gw(ctx)
        self.assertEqual(vnet_gw.gateway_type, VirtualNetworkGatewayType.EXPRESS_ROUTE)
        self.assertEqual(vnet_gw.sku_tier, 'Standard')

    @context(module_path="vpn_vnet_gw")
    def test_vpn_vnet_gw(self, ctx: AzureEnvironmentContext):
        vnet_gw = self._get_gw(ctx)
        self.assertEqual(vnet_gw.gateway_type, VirtualNetworkGatewayType.VPN)
        self.assertEqual(vnet_gw.sku_tier, 'Basic')

    def _get_gw(self, ctx: AzureEnvironmentContext) -> AzureVirtualNetworkGateway:
        vnet_gw = next((gw for gw in ctx.vnet_gateways if gw.name == 'cr2142vgw-vnetgw'), None)
        self.assertIsNotNone(vnet_gw)
        return vnet_gw
