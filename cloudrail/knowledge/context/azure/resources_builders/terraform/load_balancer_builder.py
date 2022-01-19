from typing import List

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.constants.networking import AddressProtocolVersion
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer import AzureLoadBalancer, AzureLoadBalancerSku, \
    AzureLoadBalancerSkuTier
from cloudrail.knowledge.context.azure.resources.load_balancer.load_balancer_frontend_ip_configuration import LoadBalancerFrontendIpConfiguration, \
    FrontendIpConfigurationAvailabilityZone, PrivateIpAddressAllocation
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class LoadBalancerBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureLoadBalancer:
        sku = enum_implementation(AzureLoadBalancerSku, self._get_known_value(attributes, 'sku'), AzureLoadBalancerSku.BASIC)
        sku_tier = enum_implementation(AzureLoadBalancerSkuTier, self._get_known_value(attributes, 'sku_tier'), AzureLoadBalancerSkuTier.REGIONAL)

        frontend_ip_configurations: List[LoadBalancerFrontendIpConfiguration] = []
        for fip_config in attributes.get('frontend_ip_configuration', []):
            ## Availability zones
            azs: List[FrontendIpConfigurationAvailabilityZone] = []
            default_azs = [FrontendIpConfigurationAvailabilityZone.ZONE_1,
                           FrontendIpConfigurationAvailabilityZone.ZONE_2,
                           FrontendIpConfigurationAvailabilityZone.ZONE_3]
            if sku != AzureLoadBalancerSku.STANDARD:
                azs = default_azs
            if az_string := self._get_known_value(fip_config, 'availability_zone'):
                azs_data = [FrontendIpConfigurationAvailabilityZone(az) for az in az_string.split(',')]
                if azs_data == [FrontendIpConfigurationAvailabilityZone.NO_ZONE]:
                    azs = []
                elif azs_data == [FrontendIpConfigurationAvailabilityZone.ZONE_REDUNDANT]:
                    azs = default_azs
                else:
                    azs = azs_data
            ip_alloc_value = self._get_known_value(fip_config, 'private_ip_address_allocation')
            ip_alloc = enum_implementation(PrivateIpAddressAllocation, ip_alloc_value.lower() if ip_alloc_value else None)
            ip_version = enum_implementation(AddressProtocolVersion, self._get_known_value(fip_config, 'private_ip_address_version'))

            frontend_ip_configurations.append(LoadBalancerFrontendIpConfiguration(name=fip_config['name'],
                                                                                  availability_zone=azs,
                                                                                  subnet_id=self._get_known_value(fip_config, 'subnet_id'),
                                                                                  gateway_load_balancer_frontend_ip_configuration_id=
                                                                                  self._get_known_value(fip_config, 'gateway_load_balancer_frontend_ip_configuration_id'),
                                                                                  private_ip_address=self._get_known_value(fip_config, 'private_ip_address'),
                                                                                  private_ip_address_allocation=ip_alloc,
                                                                                  private_ip_address_version=ip_version,
                                                                                  public_ip_address_id=self._get_known_value(fip_config, 'public_ip_address_id'),
                                                                                  public_ip_prefix_id=self._get_known_value(fip_config, 'public_ip_prefix_id')))

        return AzureLoadBalancer(name=attributes['name'],
                                 sku=sku,
                                 sku_tier=sku_tier,
                                 frontend_ip_configurations=frontend_ip_configurations)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_LB
