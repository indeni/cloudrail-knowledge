from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer import AzureLoadBalancer, AzureLoadBalancerSku, \
    AzureLoadBalancerSkuTier
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestLoadBalancer(AzureContextTest):

    def get_component(self):
        return 'load_balancer'

    @context(module_path="default_settings")
    def test_default_settings(self, ctx: AzureEnvironmentContext):
        load_balancer: AzureLoadBalancer = ctx.load_balancers.get('azurerm_lb.load_balancer.id')
        self.assertIsNotNone(load_balancer)
        self.assertEqual(load_balancer.name, 'cr3763-lbGateway')
        self.assertEqual(load_balancer.sku, AzureLoadBalancerSku.BASIC)
        self.assertEqual(load_balancer.sku_tier, AzureLoadBalancerSkuTier.REGIONAL)
        self.assertEqual(load_balancer.frontend_ip_configurations, [])
