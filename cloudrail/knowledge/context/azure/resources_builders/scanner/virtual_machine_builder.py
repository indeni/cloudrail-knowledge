from typing import List
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine, DataDisk, DiskSettings, OperatingSystemType, OsDisk, OsDiskCaching, \
    OsDiskStorageAccountType, SourceImageReference
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class VirtualMachineBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'virtual-machines.json'

    def do_build(self, attributes: dict) -> AzureVirtualMachine:
        properties = attributes['properties']
        os_profile = properties['osProfile']
        storage_profile = properties['storageProfile']

        ## Disk Settings
        os_disk_profile = storage_profile['osDisk']
        data_disks_list : List[DataDisk] = []
        if data_disks_list_data := storage_profile.get('dataDisks'):
            for data in data_disks_list_data:
                data_disks_list.append(DataDisk(data['name'], bool(data.get('managedDisk'))))
        os_disk = OsDisk(name=os_disk_profile['name'],
                         is_managed_disk=bool(os_disk_profile.get('managedDisk')),
                         caching=OsDiskCaching(os_disk_profile['caching']),
                         storage_account_type=enum_implementation(OsDiskStorageAccountType, os_disk_profile.get('managedDisk', {}).get('storageAccountType')))

        ## Source Image Reference
        source_image_reference = None
        if source_image_data := storage_profile.get('imageReference'):
            source_image_reference = SourceImageReference(publisher=source_image_data.get('publisher'),
                                                          offer=source_image_data.get('offer'),
                                                          sku=source_image_data.get('sku'),
                                                          version=source_image_data.get('version'))

        ## Disable Password Settings
        disable_password_authentication = None
        if os_profile_linux_config_data := os_profile.get('linuxConfiguration'):
            disable_password_authentication = os_profile_linux_config_data.get('disablePasswordAuthentication')

        return AzureVirtualMachine(name=attributes['name'],
                                   network_interface_ids=[nic_info['id'] for nic_info in properties['networkProfile']['networkInterfaces']],
                                   os_type=OperatingSystemType.WINDOWS if 'windowsConfiguration' in os_profile else OperatingSystemType.LINUX,
                                   disk_settings=DiskSettings(os_disk, data_disks_list),
                                   sku=properties['hardwareProfile']['vmSize'],
                                   source_image_reference=source_image_reference,
                                   disable_password_authentication=disable_password_authentication)
