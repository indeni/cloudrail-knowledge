import ipaddress

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestVirtualNetwork(AzureContextTest):

    def get_component(self):
        return "virtual_network"

    @context(module_path="default_settings")
    def test_express_route_vnet_gw(self, ctx: AzureEnvironmentContext):
        vnet = ctx.virtual_networks.get('/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr24601-RG/providers/'
                                        'Microsoft.Network/virtualNetworks/cr24601-vnet') or \
               ctx.virtual_networks.get('azurerm_virtual_network.vnet.id')
        self.assertIsNotNone(vnet)
        self.assertEqual(vnet.network_name, 'cr24601-vnet')
        self.assertEqual(vnet.cidr_addresses, [ipaddress.ip_network('10.5.0.0/16')])
        self.assertEqual(vnet.location, 'westeurope')
