from typing import List

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.constants.networking import AddressProtocolVersion
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer import AzureLoadBalancer, AzureLoadBalancerSku, \
    AzureLoadBalancerSkuTier
from cloudrail.knowledge.context.azure.resources.load_balancer.load_balancer_frontend_ip_configuration import LoadBalancerFrontendIpConfiguration, \
    FrontendIpConfigurationAvailabilityZone, PrivateIpAddressAllocation
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class LoadBalancerBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureLoadBalancer:
        sku: AzureLoadBalancerSku = AzureLoadBalancerSku(attributes.get('sku')) if attributes.get('sku') else AzureLoadBalancerSku.BASIC
        sku_tier: AzureLoadBalancerSkuTier = AzureLoadBalancerSkuTier(attributes.get('sku_tier')) \
            if attributes.get('sku_tier') else AzureLoadBalancerSkuTier.REGIONAL

        frontend_ip_configurations: List[LoadBalancerFrontendIpConfiguration] = []
        for conf in attributes.get('frontend_ip_configuration', []):
            azs: List[FrontendIpConfigurationAvailabilityZone] = []
            azs.extend([FrontendIpConfigurationAvailabilityZone(az) for az in conf.get('availability_zone', [])])
            if not azs:
                azs.append(FrontendIpConfigurationAvailabilityZone.ZONE_REDUNDANT)
            ip_alloc: PrivateIpAddressAllocation = PrivateIpAddressAllocation(conf.get('private_ip_address_allocation')) \
                if conf.get('private_ip_address_allocation') else None
            ip_version: AddressProtocolVersion = AddressProtocolVersion(conf.get('private_ip_address_version')) \
                if conf.get('private_ip_address_version') else None

            frontend_ip_configurations.append(LoadBalancerFrontendIpConfiguration(name=conf['name'],
                                                                                  availability_zone=azs,
                                                                                  subnet_id=conf.get('subnet_id'),
                                                                                  gateway_load_balancer_frontend_ip_configuration_id=
                                                                                  conf.get('gateway_load_balancer_frontend_ip_configuration_id'),
                                                                                  private_ip_address=conf.get('private_ip_address'),
                                                                                  private_ip_address_allocation=ip_alloc,
                                                                                  private_ip_address_version=ip_version,
                                                                                  public_ip_address_id=conf.get('public_ip_address_id'),
                                                                                  public_ip_prefix_id=conf.get('public_ip_prefix_id')))

        return AzureLoadBalancer(name=attributes['name'],
                                 sku=sku,
                                 sku_tier=sku_tier,
                                 frontend_ip_configurations=frontend_ip_configurations)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_LB
