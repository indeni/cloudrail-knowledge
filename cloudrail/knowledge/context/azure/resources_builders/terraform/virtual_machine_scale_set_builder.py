from typing import Callable, List, Optional

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface, IpConfiguration
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import DataDisk, DiskSettings, OperatingSystemType, OsDisk, OsDiskCaching, \
    OsDiskStorageAccountType
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet, Sku, SkuTier, UpgradePolicyMode, \
    SourceImageReference
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class VirtualMachineScaleSetBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualMachineScaleSet:
        os_type = OperatingSystemType.WINDOWS if self._get_known_value(attributes, 'os_profile_windows_config') else OperatingSystemType.LINUX
        return _build_vmss(attributes, os_type, 'no_os', self._get_known_value)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_VIRTUAL_MACHINE_SCALE_SET


class LinuxVirtualMachineScaleSetBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualMachineScaleSet:
        return _build_vmss(attributes, OperatingSystemType.LINUX, 'linux', self._get_known_value)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_LINUX_VIRTUAL_MACHINE_SCALE_SET


class WindowsVirtualMachineScaleSetBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureVirtualMachineScaleSet:
        return _build_vmss(attributes, OperatingSystemType.WINDOWS, 'windows', self._get_known_value)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_WINDOWS_VIRTUAL_MACHINE_SCALE_SET


def _build_vmss(attributes: dict, os_type: OperatingSystemType, vm_tf_type: str, get_known_value_function: Callable[[dict, str, Optional[any]], any]) -> AzureVirtualMachineScaleSet:
    data_disks_list : List[DataDisk] = []
    disable_password_authentication = None
    source_image_reference = None

    if vm_tf_type == 'no_os':
        ## Disk settings
        os_disk_profile = attributes['storage_profile_os_disk']
        os_disk = OsDisk(name=get_known_value_function(os_disk_profile[0], 'name'),
                         is_managed_disk=bool(get_known_value_function(os_disk_profile[0], 'managed_disk_type')),
                         caching=enum_implementation(OsDiskCaching, get_known_value_function(os_disk_profile[0], 'caching', None)),
                         storage_account_type=enum_implementation(OsDiskStorageAccountType, get_known_value_function(os_disk_profile[0], 'managed_disk_type')))
        if data_disks_list_data := get_known_value_function(attributes, 'storage_profile_data_disk'):
            for _ in data_disks_list_data:
                data_disks_list.append(DataDisk(None, os_disk.is_managed_disk))
        disk_settings = DiskSettings(os_disk, data_disks_list)

        ## SKU
        sku_data = attributes['sku'][0]
        sku = Sku(name=sku_data['name'],
                  tier=enum_implementation(SkuTier, get_known_value_function(sku_data, 'tier')),
                  capacity=sku_data['capacity'])
        instances = sku.capacity

        ## Source Image Reference
        if source_image_data := get_known_value_function(attributes, 'storage_profile_image_reference'):
            source_image_reference = SourceImageReference(publisher=get_known_value_function(source_image_data[0], 'publisher'),
                                                          offer=get_known_value_function(source_image_data[0], 'offer'),
                                                          sku=get_known_value_function(source_image_data[0], 'sku'),
                                                          version=get_known_value_function(source_image_data[0], 'version'))

        ## Disable Password Settings
        if os_profile_linux_config_data := get_known_value_function(attributes, 'os_profile_linux_config'):
            disable_password_authentication = get_known_value_function(os_profile_linux_config_data[0], 'disable_password_authentication', False)

        ## Upgrade Policy mode
        upgrade_policy_mode = enum_implementation(UpgradePolicyMode, get_known_value_function(attributes, 'upgrade_policy_mode'))

    else:
        ## Disk settings
        if data_disks_list_data := get_known_value_function(attributes, 'data_disk'):
            for _ in data_disks_list_data:
                data_disks_list.append(DataDisk(None, True))
        os_disk_data = attributes['os_disk'][0]
        disk_settings = DiskSettings(OsDisk(None,
                                            True,
                                            enum_implementation(OsDiskCaching, os_disk_data['caching']),
                                            enum_implementation(OsDiskStorageAccountType, os_disk_data['storage_account_type'])),
                                     data_disks_list)
        ## SKU
        sku = Sku(attributes['sku'], None, attributes['instances'])
        instances = attributes['instances']

        ## Source Image Reference
        if source_image_data := get_known_value_function(attributes, 'source_image_reference'):
            source_image_reference = SourceImageReference(publisher=get_known_value_function(source_image_data[0], 'publisher'),
                                                          offer=get_known_value_function(source_image_data[0], 'offer'),
                                                          sku=get_known_value_function(source_image_data[0], 'sku'),
                                                          version=get_known_value_function(source_image_data[0], 'version'))

        ## Disable Password Settings
        if vm_tf_type == 'linux':
            disable_password_authentication = get_known_value_function(attributes, 'disable_password_authentication', True)

        ## Upgrade Policy mode
        upgrade_policy_mode = enum_implementation(UpgradePolicyMode, get_known_value_function(attributes, 'upgrade_mode', 'Manual'))

    ## Networking data
    network_profile_data = attributes.get('network_profile') or attributes.get('network_interface')
    network_interfaces_config : List[AzureNetworkInterface] = []
    for network_config in network_profile_data:
        interface_name = network_config['name']
        network_security_group_id = get_known_value_function(network_config, 'network_security_group_id')
        ip_config_list : List[IpConfiguration] = []
        for ip_config in network_config['ip_configuration']:
            public_ip_id = get_known_value_function(ip_config, 'public_ip_address', {}).get('public_ip_prefix_id')
            subnet_id = get_known_value_function(ip_config, 'subnet_id')
            application_security_group_ids = get_known_value_function(ip_config, 'application_security_group_ids')
            ip_config_list.append(IpConfiguration(public_ip_id, subnet_id, None, application_security_group_ids))
        network_interfaces_config.append(AzureNetworkInterface(interface_name, ip_config_list, network_security_group_id))

    return AzureVirtualMachineScaleSet(name=attributes['name'],
                                       os_type=os_type,
                                       disk_settings=disk_settings,
                                       network_interfaces_config=network_interfaces_config,
                                       upgrade_policy_mode=upgrade_policy_mode,
                                       sku=sku,
                                       instances=instances,
                                       source_image_reference=source_image_reference,
                                       disable_password_authentication=disable_password_authentication)
