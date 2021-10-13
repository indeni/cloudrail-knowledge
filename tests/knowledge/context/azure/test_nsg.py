from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext

from test.knowledge.context.azure_context_test import AzureContextTest
from test.knowledge.context.test_context_annotation import context


class TestNetworkSecurityGroupUnused(AzureContextTest):

    def get_component(self):
        return "nsg"

    @context(module_path="nsg_unused")
    def test_nsg_unused(self, ctx: AzureEnvironmentContext):
        nsg = self._get_nsg(ctx)
        self.assertEqual(len(nsg.subnets), 0)
        self.assertEqual(len(nsg.network_interfaces), 0)

    @context(module_path="nsg_attached_to_nic")
    def test_nsg_attached_to_nic(self, ctx: AzureEnvironmentContext):
        nsg = self._get_nsg(ctx)
        nic = next((nic for nic in ctx.network_interfaces if nic.name == 'cr2106nsg-nic'), None)
        self.assertIsNotNone(nic)
        self.assertEqual(len(nsg.subnets), 0)
        self.assertEqual(len(nsg.network_interfaces), 1)
        self.assertEqual(nsg.network_interfaces[0], nic)

    @context(module_path="nsg_attached_to_subnet")
    def test_nsg_attached_to_subnet(self, ctx: AzureEnvironmentContext):
        nsg = self._get_nsg(ctx)
        subnet = next((subnet for subnet in ctx.subnets if subnet.name == 'cr2106nsg-snet'), None)
        self.assertIsNotNone(subnet)
        self.assertEqual(len(nsg.subnets), 1)
        self.assertEqual(len(nsg.network_interfaces), 0)
        self.assertEqual(nsg.subnets[0], subnet)

    @context(module_path="nsg_with_rules")
    def test_nsg_with_rules(self, ctx: AzureEnvironmentContext):
        nsg = self._get_nsg(ctx)
        self.assertEqual(len(nsg.network_security_rules), 8) # 2 + 6 default rules

    @context(module_path="nsg_with_standalone_rule")
    def test_nsg_with_standalone_rule(self, ctx: AzureEnvironmentContext):
        nsg = self._get_nsg(ctx)
        self.assertEqual(len(nsg.network_security_rules), 7) # 1 + 6 default rules

    def _get_nsg(self, ctx: AzureEnvironmentContext):
        nsg = next((nsg for nsg in ctx.net_security_groups if nsg.name in ('cr2106nsg-nsg', 'cr2460-nsg')), None)
        self.assertIsNotNone(nsg)
        return nsg
