import dataclasses
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import DiskSettings, OperatingSystemType, SourceImageReference
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine_extension import AzureVirtualMachineExtension

class SkuTier(str, Enum):
    STANDARD = 'standard'
    BASIC = 'basic'


@dataclass
class Sku:
    """
        Attributes:
            name: The SKU name
            tier: The tier of virtual machines in a scale set (Values: standard or basic)
            capacity: The number of virtual machines in the scale set
    """
    name: str
    tier: Optional[SkuTier]
    capacity: Optional[int]


class UpgradePolicyMode(Enum):
    ROLLING = 'Rolling'
    MANUAL = 'Manual'
    AUTOMATIC = 'Automatic'


class AzureVirtualMachineScaleSet(AzureResource):
    """
        Attributes:
            name: The name of the Virtual machine scale set resource.
            os_type: The VM's instances operating system. Either Windows or Linux.
            disk_settings: The disk settings which will be used for the VM's instances.
            network_interfaces_config: The network interfaces configurations which will be used for the VM's instances.
            upgrade_policy_mode: Specifies the mode of an upgrade to virtual machines in the scale set.
            sku: The SKU configuration block for the scale set.
            instances: The number of Virtual Machines in the Scale Set.
            source_image_reference: The image used in the Virtual Machine OS.
            disable_password_authentication: If Password Authentication should be disabled on this Virtual Machine Scale Set (relavant for Linux OS).
            extensions: List of extension profiles to add to the scale set.
    """

    def __init__(self,
                 name: str,
                 os_type: OperatingSystemType,
                 disk_settings: DiskSettings,
                 network_interfaces_config: List[AzureNetworkInterface],
                 upgrade_policy_mode: Optional[UpgradePolicyMode],
                 sku: Sku,
                 instances: int,
                 source_image_reference: SourceImageReference,
                 disable_password_authentication: Optional[bool]):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_MACHINE_SCALE_SET)
        self.name: str = name
        self.os_type: OperatingSystemType = os_type
        self.disk_settings: DiskSettings = disk_settings
        self.network_interfaces_config: List[AzureNetworkInterface] = network_interfaces_config
        self.upgrade_policy_mode: Optional[UpgradePolicyMode] = upgrade_policy_mode
        self.sku: Sku = sku
        self.instances: int = instances
        self.source_image_reference: SourceImageReference = source_image_reference
        self.disable_password_authentication: Optional[bool] = disable_password_authentication
        self.extensions: Optional[List[AzureVirtualMachineExtension]] = []

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

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'os_type': self.os_type.value,
                'disk_settings': dataclasses.asdict(self.disk_settings)}

    @property
    def is_diagnostics_logs_enabled(self) -> bool:
        if self.os_type == OperatingSystemType.LINUX:
            return self.extensions and \
                   any(ext.publisher in ('Microsoft.Azure.Diagnostics', 'Microsoft.OSTCExtensions') and ext.extension_type == 'LinuxDiagnostic'
                       for ext in self.extensions)
        else:
            return self.extensions and \
                   any(ext.publisher == 'Microsoft.Azure.Diagnostics' and ext.extension_type == 'IaaSDiagnostics'
                       for ext in self.extensions)
