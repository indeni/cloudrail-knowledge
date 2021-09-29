from typing import List
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine, DataDisk, DiskSettings, OperatingSystemType, OsDisk

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class VirtualMachineBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'virtual-machines.json'

    def do_build(self, attributes: dict) -> AzureVirtualMachine:
        os_profile = attributes['properties']['osProfile']
        os_disk_profile = attributes['properties']['storageProfile']['osDisk']
        data_disks_list : List[DataDisk] = []
        if data_disks_list_data := attributes['properties']['storageProfile'].get('dataDisks'):
            for data in data_disks_list_data:
                data_disks_list.append(DataDisk(data['name'], bool(data.get('managedDisk'))))
        return AzureVirtualMachine(name=attributes['name'],
                                   network_interface_ids=[nic_info['id'] for nic_info in attributes['properties']['networkProfile']['networkInterfaces']],
                                   os_type=OperatingSystemType.WINDOWS if 'windowsConfiguration' in os_profile else OperatingSystemType.LINUX,
                                   disk_settings=DiskSettings(OsDisk(os_disk_profile['name'], bool(os_disk_profile.get('managedDisk'))),
                                                              data_disks_list))
