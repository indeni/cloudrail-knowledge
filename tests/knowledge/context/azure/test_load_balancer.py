from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer import AzureLoadBalancerSku, \
    AzureLoadBalancerSkuTier
from cloudrail.knowledge.context.azure.resources.load_balancer.load_balancer_frontend_ip_configuration import FrontendIpConfigurationAvailabilityZone, \
    PrivateIpAddressAllocation, AddressProtocolVersion
from cloudrail.knowledge.context.mergeable import EntityOrigin
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestLoadBalancer(AzureContextTest):

    def get_component(self):
        return 'load_balancer'

    @context(module_path="default_settings")
    def test_default_settings(self, ctx: AzureEnvironmentContext):
        load_balancer = next((lb for lb in ctx.load_balancers if lb.name == 'cr3763-lbGateway'), None)
        self.assertIsNotNone(load_balancer)
        self.assertEqual(load_balancer.name, 'cr3763-lbGateway')
        self.assertEqual(load_balancer.sku, AzureLoadBalancerSku.BASIC)
        self.assertEqual(load_balancer.sku_tier, AzureLoadBalancerSkuTier.REGIONAL)
        self.assertEqual(load_balancer.frontend_ip_configurations, [])

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        load_balancer = next((lb for lb in ctx.load_balancers if lb.name == 'cr3763-lbGateway'), None)
        self.assertIsNotNone(load_balancer)
        self.assertEqual(load_balancer.sku, AzureLoadBalancerSku.GATEWAY)
        self.assertEqual(load_balancer.sku_tier, AzureLoadBalancerSkuTier.REGIONAL)
        self.assertTrue(len(load_balancer.frontend_ip_configurations), 1)
        fip_config = load_balancer.frontend_ip_configurations[0]
        self.assertEqual(fip_config.availability_zone, [FrontendIpConfigurationAvailabilityZone.ZONE_1,
                                                        FrontendIpConfigurationAvailabilityZone.ZONE_2,
                                                        FrontendIpConfigurationAvailabilityZone.ZONE_3])
        self.assertEqual(fip_config.name, 'cr3763-lbGateway-front')
        self.assertIsNone(fip_config.gateway_load_balancer_frontend_ip_configuration_id)
        self.assertIsNone(fip_config.public_ip_address_id)
        self.assertIsNone(fip_config.public_ip_prefix_id)
        if load_balancer.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(fip_config.private_ip_address_allocation, PrivateIpAddressAllocation.DYNAMIC)
            self.assertEqual(fip_config.private_ip_address_version, AddressProtocolVersion.IP_V4)
            self.assertEqual(fip_config.private_ip_address, '10.0.1.4')
            self.assertEqual(fip_config.subnet_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3763-rg/providers/Microsoft.Network/virtualNetworks/cr3763-vnet/subnets/cr3763-subnet')
        else:
            self.assertIsNone(fip_config.private_ip_address)
            self.assertIsNone(fip_config.private_ip_address_allocation)
            self.assertIsNone(fip_config.private_ip_address_version)
            self.assertEqual(fip_config.subnet_id, 'azurerm_subnet.test.id')

        load_balancer = next((lb for lb in ctx.load_balancers if lb.name == 'cr3763-lb'), None)
        self.assertIsNotNone(load_balancer)
        self.assertEqual(load_balancer.sku, AzureLoadBalancerSku.STANDARD)
        self.assertEqual(load_balancer.sku_tier, AzureLoadBalancerSkuTier.REGIONAL)
        self.assertTrue(len(load_balancer.frontend_ip_configurations), 1)
        fip_config = load_balancer.frontend_ip_configurations[0]
        self.assertEqual(fip_config.availability_zone, [FrontendIpConfigurationAvailabilityZone.ZONE_1,
                                                        FrontendIpConfigurationAvailabilityZone.ZONE_2,
                                                        FrontendIpConfigurationAvailabilityZone.ZONE_3])
        self.assertEqual(fip_config.name, 'cr3763-lb-front')
        self.assertIsNone(fip_config.gateway_load_balancer_frontend_ip_configuration_id)
        self.assertIsNone(fip_config.public_ip_address_id)
        self.assertIsNone(fip_config.public_ip_prefix_id)
        self.assertEqual(fip_config.private_ip_address, '10.0.1.25')
        self.assertEqual(fip_config.private_ip_address_allocation, PrivateIpAddressAllocation.STATIC)
        self.assertEqual(fip_config.private_ip_address_version, AddressProtocolVersion.IP_V4)
        if load_balancer.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(fip_config.subnet_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3763-rg/providers/Microsoft.Network/virtualNetworks/cr3763-vnet/subnets/cr3763-subnet')
        else:
            self.assertEqual(fip_config.subnet_id, 'azurerm_subnet.test.id')

        load_balancer = next((lb for lb in ctx.load_balancers if lb.name == 'cr3763-lb2'), None)
        self.assertIsNotNone(load_balancer)
        self.assertEqual(load_balancer.sku, AzureLoadBalancerSku.STANDARD)
        self.assertEqual(load_balancer.sku_tier, AzureLoadBalancerSkuTier.REGIONAL)
        self.assertTrue(len(load_balancer.frontend_ip_configurations), 1)
        fip_config = load_balancer.frontend_ip_configurations[0]
        self.assertEqual(fip_config.availability_zone, [])
        self.assertEqual(fip_config.name, 'cr3763-lb-front2')
        self.assertIsNone(fip_config.gateway_load_balancer_frontend_ip_configuration_id)
        self.assertIsNone(fip_config.public_ip_address_id)
        self.assertIsNone(fip_config.private_ip_address)
        self.assertIsNone(fip_config.subnet_id)
        if load_balancer.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(fip_config.private_ip_address_allocation, PrivateIpAddressAllocation.DYNAMIC)
            self.assertEqual(fip_config.private_ip_address_version, AddressProtocolVersion.IP_V4)
            self.assertEqual(fip_config.public_ip_prefix_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3763-rg/providers/Microsoft.Network/publicIPPrefixes/cr3763-publicIPPrefix')
        else:
            self.assertIsNone(fip_config.private_ip_address_allocation)
            self.assertIsNone(fip_config.private_ip_address_version)
            self.assertEqual(fip_config.public_ip_prefix_id, 'azurerm_public_ip_prefix.test.id')

        load_balancer = next((lb for lb in ctx.load_balancers if lb.name == 'cr3763-lb3'), None)
        self.assertIsNotNone(load_balancer)
        self.assertEqual(load_balancer.sku, AzureLoadBalancerSku.STANDARD)
        self.assertEqual(load_balancer.sku_tier, AzureLoadBalancerSkuTier.REGIONAL)
        self.assertTrue(len(load_balancer.frontend_ip_configurations), 1)
        fip_config = load_balancer.frontend_ip_configurations[0]
        self.assertEqual(fip_config.availability_zone, [])
        self.assertEqual(fip_config.name, 'cr3763-lb-front3')
        self.assertIsNone(fip_config.private_ip_address)
        self.assertIsNone(fip_config.subnet_id)
        self.assertIsNone(fip_config.private_ip_address_version)
        self.assertIsNone(fip_config.public_ip_prefix_id)
        if load_balancer.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(fip_config.private_ip_address_allocation, PrivateIpAddressAllocation.DYNAMIC)
            self.assertEqual(fip_config.gateway_load_balancer_frontend_ip_configuration_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3763-rg/providers/Microsoft.Network/loadBalancers/cr3763-lbGateway/frontendIPConfigurations/cr3763-lbGateway-front')
            self.assertEqual(fip_config.public_ip_address_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3763-rg/providers/Microsoft.Network/publicIPAddresses/cr3763-publicIP')
        else:
            self.assertIsNone(fip_config.private_ip_address_allocation)
            self.assertIsNone(fip_config.private_ip_address_version)
            self.assertIsNone(fip_config.gateway_load_balancer_frontend_ip_configuration_id)
