from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.base_context_builders.base_terraform_builder import BaseTerraformBuilder


class AzureTerraformBuilder(BaseTerraformBuilder):

    def do_build(self, attributes: dict):
        pass

    def get_service_name(self):
        pass

    def _build(self) -> List[AzureResource]:
        all_attributes = self.resources.get(self.get_service_name().value)
        if not all_attributes:
            return []

        result = []
        for attributes in all_attributes:
            build_result = self._build_and_map_action(attributes)
            for resource in build_result if isinstance(build_result, list) else [build_result]:
                if resource:
                    self._set_common_attributes(resource, attributes)
                    result.append(resource)

        return result

    def _set_common_attributes(self, resource: AzureResource, attributes: dict):
        if not isinstance(resource, AzureResource):
            return
        resource.subscription_id = attributes['subscription_id']
        resource.location = self._get_normalized_azure_location(attributes.get('location'))
        resource.resource_group_name = attributes.get('resource_group_name')
        resource.tenant_id = attributes['tenant_id']
        if resource.is_tagable:
            resource.tags = attributes.get('tags')
        if not resource.get_id() and (_id := attributes.get('id')):
            resource.set_id(_id)
            resource.with_aliases(_id)

    @staticmethod
    def _get_normalized_azure_location(location: Optional[str]) -> Optional[str]:
        # Following map based on https://github.com/claranet/terraform-azurerm-regions/blob/master/REGIONS.md
        location_dict_map = {
            'eastus': 'East US',
            'eastus2': 'East US 2',
            'southcentralus': 'South Central US',
            'westus2': 'West US 2',
            'australiaeast': 'Australia East',
            'southeastasia': 'Southeast Asia',
            'northeurope': 'North Europe',
            'uksouth': 'UK South',
            'westeurope': 'West Europe',
            'centralus': 'Central US',
            'northcentralus': 'North Central US',
            'westus': 'West US',
            'southafricanorth': 'South Africa North',
            'centralindia': 'Central India',
            'eastasia': 'East Asia',
            'japaneast': 'Japan East',
            'koreacentral': 'Korea Central',
            'canadacentral': 'Canada Central',
            'francecentral': 'France Central',
            'germanywestcentral': 'Germany West Central',
            'norwayeast': 'Norway East',
            'switzerlandnorth': 'Switzerland North',
            'uaenorth': 'UAE North',
            'brazilsouth': 'Brazil South',
            'asia': 'Asia',
            'asiapacific': 'Asia Pacific',
            'australia': 'Australia',
            'brazil': 'Brazil',
            'canada': 'Canada',
            'europe': 'Europe',
            'global': 'Global',
            'india': 'India',
            'japan': 'Japan',
            'uk': 'United Kingdom',
            'unitedstates': 'United States',
            'westcentralus': 'West Central US',
            'southafricawest': 'South Africa West',
            'australiacentral': 'Australia Central',
            'australiacentral2': 'Australia Central 2',
            'australiasoutheast': 'Australia Southeast',
            'japanwest': 'Japan West',
            'koreasouth': 'Korea South',
            'southindia': 'South India',
            'westindia': 'West India',
            'canadaeast': 'Canada East',
            'francesouth': 'France South',
            'germanynorth': 'Germany North',
            'norwaywest': 'Norway West',
            'switzerlandwest': 'Switzerland West',
            'ukwest': 'UK West',
            'uaecentral': 'UAE Central',
            'brazilsoutheast': 'Brazil Southeast',
            'germanynortheast': 'Germany Northeast',
            'germanycentral': 'Germany Central',
            'chinanorth': 'China North',
            'chinaeast': 'China East',
            'chinaeast2': 'China East 2',
            'chinanorth2': 'China North 2',
        }
        if location:
            return location_dict_map[location]
        return None
