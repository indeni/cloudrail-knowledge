from typing import Callable, List, Optional
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine, DataDisk, DiskSettings, OperatingSystemType, OsDisk, OsDiskCaching, \
    OsDiskStorageAccountType, SourceImageReference
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


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
    source_image_reference = None
    disable_password_authentication = None

    if vm_tf_type == 'no_os':
        ## Disk Settings
        os_disk_profile = attributes['storage_os_disk'][0]
        os_disk = OsDisk(name=os_disk_profile['name'],
                         is_managed_disk=os_disk_profile.get('vhd_uri') in (None, ''),
                         caching=enum_implementation(OsDiskCaching, get_known_value_function(os_disk_profile, 'caching', None)),
                         storage_account_type=enum_implementation(OsDiskStorageAccountType, get_known_value_function(os_disk_profile, 'managed_disk_type')))
        if data_disks_list_data := get_known_value_function(attributes, 'storage_data_disk'):
            for data in data_disks_list_data:
                data_disks_list.append(DataDisk(data['name'], os_disk.is_managed_disk))
        disk_settings=DiskSettings(os_disk, data_disks_list)

        ## SKU
        sku = attributes['vm_size']

        ## Source Image Reference
        if source_image_data := get_known_value_function(attributes, 'storage_image_reference'):
            source_image_reference = SourceImageReference(publisher=get_known_value_function(source_image_data[0], 'publisher'),
                                                          offer=get_known_value_function(source_image_data[0], 'offer'),
                                                          sku=get_known_value_function(source_image_data[0], 'sku'),
                                                          version=get_known_value_function(source_image_data[0], 'version'))

        ## Disable Password Settings
        if os_profile_linux_config_data := get_known_value_function(attributes, 'os_profile_linux_config'):
            disable_password_authentication = get_known_value_function(os_profile_linux_config_data[0], 'disable_password_authentication')
    else:
        ## Disk Settings
        os_disk_profile = attributes['os_disk'][0]
        disk_settings = DiskSettings(OsDisk(name=os_disk_profile.get('name'),
                                            is_managed_disk=True,
                                            caching=enum_implementation(OsDiskCaching, get_known_value_function(os_disk_profile, 'caching', None)),
                                            storage_account_type=enum_implementation(OsDiskStorageAccountType,
                                                                                     get_known_value_function(os_disk_profile, 'storage_account_type'))),
                                     data_disks_list)

        ## SKU
        sku = attributes['size']

        ## Source Image Reference
        if source_image_data := get_known_value_function(attributes, 'source_image_reference'):
            source_image_reference = SourceImageReference(publisher=get_known_value_function(source_image_data[0], 'publisher'),
                                                          offer=get_known_value_function(source_image_data[0], 'offer'),
                                                          sku=get_known_value_function(source_image_data[0], 'sku'),
                                                          version=get_known_value_function(source_image_data[0], 'version'))

        ## Disable Password Settings
        if vm_tf_type == 'linux':
            disable_password_authentication = get_known_value_function(attributes, 'disable_password_authentication', True)
    return AzureVirtualMachine(name=attributes['name'],
                               network_interface_ids=attributes['network_interface_ids'],
                               os_type=os_type,
                               disk_settings=disk_settings,
                               sku=sku,
                               source_image_reference=source_image_reference,
                               disable_password_authentication=disable_password_authentication)
