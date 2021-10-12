from typing import Callable, List, Optional
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine, DataDisk, DiskSettings, OperatingSystemType, OsDisk

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class VirtualMachineBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualMachine:
        os_type = OperatingSystemType.WINDOWS if self._get_known_value(attributes, 'os_profile_windows_config') else OperatingSystemType.LINUX
        return _build_vm(attributes, os_type, 'no_os', self._get_known_value)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_MACHINE


class LinuxVirtualMachineBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualMachine:
        return _build_vm(attributes, OperatingSystemType.LINUX, 'linux', self._get_known_value)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_LINUX_VIRTUAL_MACHINE


class WindowsVirtualMachineBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualMachine:
        return _build_vm(attributes, OperatingSystemType.WINDOWS, 'windows', self._get_known_value)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_WINDOWS_VIRTUAL_MACHINE


def _build_vm(attributes: dict, os_type: OperatingSystemType, vm_tf_type: str, get_known_value_function: Callable[[dict, str, Optional[any]], any]) -> AzureVirtualMachine:
    data_disks_list : List[DataDisk] = []
    if vm_tf_type == 'no_os':
        os_disk_profile = attributes['storage_os_disk']
        os_disk = OsDisk(os_disk_profile[0]['name'], os_disk_profile[0].get('vhd_uri') is None)
        if data_disks_list_data := get_known_value_function(attributes, 'storage_data_disk'):
            for data in data_disks_list_data:
                data_disks_list.append(DataDisk(data['name'], os_disk.is_managed_disk))
        disk_settings=DiskSettings(os_disk, data_disks_list)
    else:
        os_disk_profile = attributes['os_disk']
        disk_settings = DiskSettings(OsDisk(os_disk_profile[0].get('name'), True), data_disks_list)
    return AzureVirtualMachine(name=attributes['name'],
                               network_interface_ids=attributes['network_interface_ids'],
                               os_type=os_type,
                               disk_settings=disk_settings)
