from typing import List

from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import (AzureNetworkInterface, IpConfiguration)
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import (DataDisk, DiskSettings, OperatingSystemType, OsDisk)
from cloudrail.knowledge.context.azure.resources.vmss.azure_virtual_machine_scale_set import AzureVirtualMachineScaleSet
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class VirtualMachineScaleSetBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'vmss-list.json'

    def do_build(self, attributes: dict) -> AzureVirtualMachineScaleSet:
        # Preparing data sections:
        virtual_machine_settings = attributes['properties']['virtualMachineProfile']
        os_profile = virtual_machine_settings['osProfile']
        storage_data = virtual_machine_settings['storageProfile']
        os_disk_data = storage_data['osDisk']
        networking_data = virtual_machine_settings['networkProfile']['networkInterfaceConfigurations']

        # Collecting info about data disks:
        data_disks_list: List[DataDisk] = []
        if data_disks_list_data := storage_data.get('dataDisks'):
            for data in data_disks_list_data:
                data_disks_list.append(DataDisk(None, bool(data.get('managedDisk'))))

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

        return AzureVirtualMachineScaleSet(name=attributes['name'],
                                           os_type=OperatingSystemType.WINDOWS if 'windowsConfiguration' in os_profile else OperatingSystemType.LINUX,
                                           disk_settings=DiskSettings(OsDisk(os_disk_data.get('name'), bool(os_disk_data.get('managedDisk'))),
                                                                      data_disks_list),
                                           network_interfaces_config=network_interfaces_config_list)
