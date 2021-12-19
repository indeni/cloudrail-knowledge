from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.storage.azure_data_lake_store import AzureDataLakeStore, DataLakeStoreTier
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.context.field_active import FieldActive


class AzureDataLakeStoreBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict):
        tier: DataLakeStoreTier = DataLakeStoreTier(attributes['tier']) if 'tier' in attributes else DataLakeStoreTier.NONE
        encryption_state: FieldActive = FieldActive(attributes.get('encryption_state', 'Enabled'))
        encryption_type: str = self._get_known_value(attributes, 'encryption_type') or ('ServiceManaged' if encryption_state == FieldActive.ENABLED else '')
        firewall_allow_azure_ips: FieldActive = FieldActive(attributes.get('firewall_allow_azure_ips', 'Enabled'))
        firewall_state: FieldActive = FieldActive(attributes.get('firewall_state', 'Enabled'))
        identity = None
        if identity_data := self._get_known_value(attributes, 'identity'):
            identity = self._get_known_value(identity_data[0], 'type', 'SystemAssigned')
        return AzureDataLakeStore(name=attributes['name'],
                                  tier=tier,
                                  encryption_state=encryption_state,
                                  encryption_type=encryption_type,
                                  identity=identity,
                                  firewall_allow_azure_ips=firewall_allow_azure_ips,
                                  firewall_state=firewall_state)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_DATA_LAKE_STORE
