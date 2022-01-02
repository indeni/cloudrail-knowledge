from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.batch_management.azure_batch_account import AzureBatchAccount, BatchAccountPoolAllocationMode, BatchAccountKeyVaultReference

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class BatchAccountBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureBatchAccount:
        key_vault_reference = None
        if key_vault_ref_data := self._get_known_value(attributes, 'key_vault_reference'):
            key_vault_reference=BatchAccountKeyVaultReference(name=attributes['name'],
                                                              id=key_vault_ref_data[0]['id'],
                                                              url=key_vault_ref_data[0]['url'])
        return AzureBatchAccount(name=attributes['name'],
                                 pool_allocation_mode=BatchAccountPoolAllocationMode(self._get_known_value(attributes, 'pool_allocation_mode', 'BatchService')),
                                 public_network_access_enabled=self._get_known_value(attributes, 'public_network_access_enabled', True),
                                 key_vault_reference=key_vault_reference,
                                 storage_account_id=attributes.get('storage_account_id'))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_BATCH_ACCOUNT
