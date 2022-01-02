from typing import List

from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import (AzureNetworkInterface, IpConfiguration)
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import (DataDisk, DiskSettings, OperatingSystemType, OsDisk, OsDiskCaching, \
    OsDiskStorageAccountType, SourceImageReference)
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet, SkuTier, UpgradePolicyMode, Sku
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class VirtualMachineScaleSetBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'vmss-list.json'

    def do_build(self, attributes: dict) -> AzureVirtualMachineScaleSet:
        # Preparing data sections:
        properties = attributes['properties']
        virtual_machine_settings = properties['virtualMachineProfile']
        os_profile = virtual_machine_settings['osProfile']
        storage_data = virtual_machine_settings['storageProfile']
        os_disk_data = storage_data['osDisk']
        networking_data = virtual_machine_settings['networkProfile']['networkInterfaceConfigurations']

        # Collecting info about data disks:
        data_disks_list: List[DataDisk] = []
        if data_disks_list_data := storage_data.get('dataDisks'):
            for data in data_disks_list_data:
                data_disks_list.append(DataDisk(None, bool(data.get('managedDisk'))))

        os_disk = OsDisk(name=os_disk_data.get('name'),
                         is_managed_disk=bool(os_disk_data.get('managedDisk')),
                         caching=OsDiskCaching(os_disk_data['caching']),
                         storage_account_type=enum_implementation(OsDiskStorageAccountType, os_disk_data.get('managedDisk', {}).get('storageAccountType')))

        # Collecting data about network interfaces configuration:
        network_interfaces_config_list: List[AzureNetworkInterface] = []
        for network_config in networking_data:
            network_properties = network_config['properties']
            ip_config_properties = network_properties['ipConfigurations']
            interface_name = network_config['name']
            network_security_group_id = network_properties.get('networkSecurityGroup')
            network_interace_ip_config_list : List[IpConfiguration] = []
            for ip_config in ip_config_properties:
                public_ip_id = ip_config['properties'].get('publicIPAddressConfiguration', {}).get('id')
                subnet_id = ip_config['properties']['subnet']['id']
                application_security_groups_ids = ip_config['properties'].get('applicationGatewayBackendAddressPools', {}).get('id')
                network_interace_ip_config_list.append(IpConfiguration(public_ip_id, subnet_id, None, application_security_groups_ids))
            network_interfaces_config_list.append(AzureNetworkInterface(interface_name,
                                                                        network_interace_ip_config_list,
                                                                        network_security_group_id))

        ## SKU
        sku_data = attributes['sku']
        sku = Sku(name=sku_data['name'],
                  tier=enum_implementation(SkuTier, sku_data['tier']),
                  capacity=sku_data['capacity'])
        instances = sku.capacity

        ## Source Image Reference
        source_image_reference = None
        if source_image_data := storage_data.get('imageReference'):
            source_image_reference = SourceImageReference(publisher=source_image_data.get('publisher'),
                                                          offer=source_image_data.get('offer'),
                                                          sku=source_image_data.get('sku'),
                                                          version=source_image_data.get('version'))

        ## Disable Password Settings
        disable_password_authentication = None
        if os_profile_linux_config_data := os_profile.get('linuxConfiguration'):
            disable_password_authentication = os_profile_linux_config_data.get('disablePasswordAuthentication')

        return AzureVirtualMachineScaleSet(name=attributes['name'],
                                           os_type=OperatingSystemType.WINDOWS if 'windowsConfiguration' in os_profile else OperatingSystemType.LINUX,
                                           disk_settings=DiskSettings(os_disk, data_disks_list),
                                           network_interfaces_config=network_interfaces_config_list,
                                           upgrade_policy_mode=enum_implementation(UpgradePolicyMode, properties.get('upgradePolicy', {}).get('mode')),
                                           sku=sku,
                                           instances=instances,
                                           source_image_reference=source_image_reference,
                                           disable_password_authentication=disable_password_authentication)
