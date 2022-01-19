from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer_nat_rule import AzureLoadBalancerNatRuleProtocol
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestLoadBalancerNatRule(AzureContextTest):

    def get_component(self):
        return "load_balancer_nat_rule"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        lb_nat_rule = next((rule for rule in ctx.load_balancer_nat_rules if rule.name == 'cr3765-natrule1'), None)
        self.assertIsNotNone(lb_nat_rule)
        self.assertTrue(lb_nat_rule.loadbalancer_id in (
            '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3765-rg/providers/Microsoft.Network/loadBalancers/cr3765-lb3',
            'azurerm_lb.test3.id'))
        self.assertTrue(lb_nat_rule.frontend_ip_configuration_name == 'cr3765-lb-front3')
        self.assertEqual(lb_nat_rule.protocol, AzureLoadBalancerNatRuleProtocol.TCP)
        self.assertEqual(lb_nat_rule.frontend_port, 3389)
        self.assertEqual(lb_nat_rule.backend_port, 3389)
        self.assertEqual(lb_nat_rule.idle_timeout_in_minutes, 4)
        self.assertFalse(lb_nat_rule.enable_floating_ip)
        self.assertFalse(lb_nat_rule.enable_tcp_reset)
