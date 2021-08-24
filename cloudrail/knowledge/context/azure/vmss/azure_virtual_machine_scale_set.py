from typing import List, Optional

from cloudrail.knowledge.context.azure.vm.azure_virtual_machine import DiskSettings, OperatingSystemType
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.network.azure_network_interface import AzureNetworkInterface


class AzureVirtualMachineScaleSet(AzureResource):
    """
        Attributes:
            name: The name of the Virtual machine scale set resource.
            os_type: The VM's instances operating system. Either Windows or Linux.
            disk_settings: The disk settings which will be used for the VM's instances.
            network_interfaces_config: The network interfaces configurations which will be used for the VM's instances.
    """
    def __init__(self, name: str, os_type: OperatingSystemType, disk_settings: DiskSettings, network_interfaces_config: List[AzureNetworkInterface]):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_MACHINE_SCALE_SET)
        self.name: str = name
        self.os_type: OperatingSystemType = os_type
        self.disk_settings: DiskSettings = disk_settings
        self.network_interfaces_config: List[AzureNetworkInterface] = network_interfaces_config

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self.get_id()}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_type(self, is_plural: bool = False) -> str:
        return 'Virtual machine scale set' + ('s' if is_plural else '')
