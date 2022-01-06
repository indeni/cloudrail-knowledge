from cloudrail.knowledge.context.azure.resources.network.azure_load_balancer_probe import AzureLoadBalancerProbeProtocol
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestLoadBalancerProbe(AzureContextTest):

    def get_component(self):
        return "load_balancer_probe"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        lb_probe_1 = next((probe for probe in ctx.load_balancer_probes if probe.name == 'cr3765-probe1'), None)
        self.assertIsNotNone(lb_probe_1)
        self.assertEqual(lb_probe_1.protocol, AzureLoadBalancerProbeProtocol.HTTP)
        self.assertEqual(lb_probe_1.port, 80)
        self.assertEqual(lb_probe_1.request_path, '/health')
        self.assertEqual(lb_probe_1.interval_in_seconds, 15)
        self.assertEqual(lb_probe_1.number_of_probes, 2)
        self.assertTrue(lb_probe_1.loadbalancer_id in (
            '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3765-rg/providers/Microsoft.Network/loadBalancers/cr3765-lb3',
            'azurerm_lb.test3.id'))
        lb_probe_2 = next((probe for probe in ctx.load_balancer_probes if probe.name == 'cr3765-probe2'), None)
        self.assertIsNotNone(lb_probe_2)
        self.assertEqual(lb_probe_2.protocol, AzureLoadBalancerProbeProtocol.HTTPS)
        self.assertEqual(lb_probe_2.port, 8443)
        self.assertEqual(lb_probe_2.request_path, '/healths')
