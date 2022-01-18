from typing import List
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer import AzureLoadBalancer, AzureLoadBalancerSku, AzureLoadBalancerSkuTier, \
    LoadBalancerFrontendIpConfiguration
from cloudrail.knowledge.context.azure.resources.load_balancer.load_balancer_frontend_ip_configuration import PrivateIpAddressAllocation, AddressProtocolVersion, \
    FrontendIpConfigurationAvailabilityZone
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class LoadBalancerBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-load-balancers.json'

    def do_build(self, attributes: dict) -> AzureLoadBalancer:
        properties = attributes['properties']

        ## SKU Data
        sku_data = attributes['sku']
        sku = enum_implementation(AzureLoadBalancerSku, sku_data['name'])
        sku_tier = enum_implementation(AzureLoadBalancerSkuTier, sku_data['tier'])

        ## FrontEnd IP Configurations
        frontend_ip_configurations: List[LoadBalancerFrontendIpConfiguration] = []
        for fip_config in properties['frontendIPConfigurations']:

            ## Availability Zones
            availability_zones: List[FrontendIpConfigurationAvailabilityZone] = []
            for zone in fip_config.get('zones', []):
                availability_zones.append(enum_implementation(FrontendIpConfigurationAvailabilityZone, zone))

            fip_config_properties = fip_config['properties']
            private_ip_address_allocation_value = fip_config_properties.get('privateIPAllocationMethod')
            private_ip_address_allocation=enum_implementation(PrivateIpAddressAllocation, private_ip_address_allocation_value.lower()
                                                              if private_ip_address_allocation_value else None)
            frontend_ip_configurations.append(LoadBalancerFrontendIpConfiguration(name=fip_config['name'],
                                                                                  availability_zone=availability_zones,
                                                                                  subnet_id=fip_config_properties.get('subnet', {}).get('id'),
                                                                                  gateway_load_balancer_frontend_ip_configuration_id=\
                                                                                      fip_config_properties.get('gatewayLoadBalancer', {}).get('id'),
                                                                                  private_ip_address=fip_config_properties.get('privateIPAddress'),
                                                                                  private_ip_address_allocation=private_ip_address_allocation,
                                                                                  private_ip_address_version=enum_implementation(AddressProtocolVersion,
                                                                                                                                 fip_config_properties.get('privateIPAddressVersion')),
                                                                                  public_ip_address_id=fip_config_properties.get('publicIPAddress', {}).get('id'),
                                                                                  public_ip_prefix_id=fip_config_properties.get('publicIPPrefix', {}).get('id')))

        return AzureLoadBalancer(name=attributes['name'],
                                 sku=sku,
                                 sku_tier=sku_tier,
                                 frontend_ip_configurations=frontend_ip_configurations)
