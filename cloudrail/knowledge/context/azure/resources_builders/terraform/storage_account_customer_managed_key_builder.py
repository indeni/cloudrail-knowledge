from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_customer_managed_key import AzureStorageAccountCustomerManagedKey
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class StorageAccountCustomerManagedKeyBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureStorageAccountCustomerManagedKey:
        storage_account_id = attributes["storage_account_id"]
        key_vault_uri = None
        key_vault_id = attributes["key_vault_id"]
        key_name = attributes["key_name"]

        return AzureStorageAccountCustomerManagedKey(storage_account_id=storage_account_id,
                                                     key_vault_uri=key_vault_uri,
                                                     key_vault_id=key_vault_id,
                                                     key_name=key_name)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_STORAGE_ACCOUNT_CUSTOMER_MANAGED_KEY
