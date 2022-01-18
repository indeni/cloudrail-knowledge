from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestNetworkInterfaceNatRuleAssociation(AzureContextTest):

    def get_component(self):
        return "network_interface_nat_rule_association"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        nic_nat_rule_assoc = next((nic for nic in ctx.network_interface_nat_rule_associations
                                   if nic.ip_configuration_name == 'ipconfig001'), None)
        self.assertIsNotNone(nic_nat_rule_assoc)
        self.assertTrue(nic_nat_rule_assoc.nat_rule_id, (
            '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3765-rg/providers/Microsoft.Network/loadBalancers/cr3765-lb3/inboundNatRules/cr3765-natrule1',
            'azurerm_lb_nat_rule.test31.id'
        ))
        self.assertTrue(nic_nat_rule_assoc.network_interface_id, (
            '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3765-rg/providers/Microsoft.Network/networkInterfaces/cr3765-nic',
            'azurerm_network_interface.nic.id'
        ))
