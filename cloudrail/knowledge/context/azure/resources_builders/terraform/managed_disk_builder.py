from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.disk.azure_managed_disk import AzureManagedDisk, ManagedDiskCreateOption, StorageAccountType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class ManagedDiskBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureManagedDisk:
        disk_encryption_enabled = False
        if encryption_settings := self._get_known_value(attributes, 'encryption_settings'):
            disk_encryption_enabled = encryption_settings[0]['enabled']
        return AzureManagedDisk(name=attributes['name'], storage_account_type=StorageAccountType(attributes['storage_account_type']),
                                create_option=ManagedDiskCreateOption(attributes['create_option']), disk_encryption_set_id=attributes['disk_encryption_set_id'],
                                disk_encryption_enabled=disk_encryption_enabled)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MANAGED_DISK
