from cloudrail.knowledge.context.azure.resources.disk.azure_managed_disk import AzureManagedDisk, ManagedDiskCreateOption, StorageAccountType
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class ManagedDiskBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'disks-list.json'

    def do_build(self, attributes: dict) -> AzureManagedDisk:
        properties = attributes['properties']
        return AzureManagedDisk(name=attributes['name'],
                                storage_account_type=StorageAccountType(attributes['sku']['name']),
                                create_option=ManagedDiskCreateOption(properties['creationData']['createOption'],),
                                disk_encryption_set_id=properties['encryption'].get('diskEncryptionSetId'),
                                disk_encryption_enabled=properties.get('encryptionSettingsCollection', {}).get('enabled'))
