from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import dataclasses
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network_resource import NetworkResource
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine_extension import AzureVirtualMachineExtension


class OsDiskCaching(Enum):
    NONE = 'None'
    READ_ONLY = 'ReadOnly'
    READ_WRITE = 'ReadWrite'


class OsDiskStorageAccountType(Enum):
    STANDARDLRS = 'Standard_LRS'
    STANDARDSSD_LRS = 'StandardSSD_LRS'
    PREMIUMLRS = 'Premium_LRS'


@dataclass
class OsDisk:
    """
        Attributes:
            name: Name of the disk.
            is_managed_disk: An indication if the disk is managed or not.
            caching: The Type of Caching which should be used for the Internal OS Disk.
            storage_account_type: The Type of Storage Account which should back this the Internal OS Disk.
    """
    name: Optional[str]
    is_managed_disk: bool
    caching: OsDiskCaching
    storage_account_type: Optional[OsDiskStorageAccountType]


@dataclass
class SourceImageReference:
    """
        Attributes:
            publisher: Specifies the publisher of the image used to create the virtual machines.
            offer: Specifies the offer of the image used to create the virtual machines.
            sku: Specifies the SKU of the image used to create the virtual machines.
            version: Specifies the version of the image used to create the virtual machines.
    """
    publisher: str
    offer: str
    sku: str
    version: str


@dataclass
class DataDisk:
    name: Optional[str]
    is_managed_disk: bool


@dataclass
class DiskSettings:
    os_disk: OsDisk
    data_disks: Optional[List[DataDisk]]


class OperatingSystemType(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'


class AzureVirtualMachine(NetworkResource):
    """
        Attributes:
            name: The name of this Public IP.
            network_interface_ids: A list of Network Interface ID's which are associated with the Virtual Machine.
            os_type: The VM's operating system. Either Windows or Linux.
            disk_settings: Information about the disks used by this Virtual Machine.
            sku: The SKU name of this Virtual Machine.
            source_image_reference: The image used for the Virtual Machine OS.
            disable_password_authentication: If Password Authentication should be disabled on this Virtual Machine (relevant only for Linux OS).

    """

    def __init__(self,
                 name: str,
                 network_interface_ids: List[str],
                 os_type: OperatingSystemType,
                 disk_settings: DiskSettings,
                 sku: str,
                 source_image_reference: SourceImageReference,
                 disable_password_authentication: Optional[bool]):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_MACHINE)
        self.name: str = name
        self.network_interface_ids: List[str] = network_interface_ids
        self.os_type: OperatingSystemType = os_type
        self.disk_settings: DiskSettings = disk_settings
        self.sku: str = sku
        self.source_image_reference: SourceImageReference = source_image_reference
        self.disable_password_authentication: Optional[bool] = disable_password_authentication
        self.extensions: Optional[List[AzureVirtualMachineExtension]] = []

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}' \
               f'/providers/Microsoft.Compute/virtualMachines/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_type(self, is_plural: bool = False) -> str:
        return 'Virtual Machine' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'network_interface_ids': self.network_interface_ids,
                'os_type': self.os_type.value,
                'disk_settings': dataclasses.asdict(self.disk_settings),
                'extesions': [ext.to_drift_detection_object() for ext in self.extensions],
                'disable_password_authentication': self.disable_password_authentication,
                'source_image_reference': dataclasses.asdict(self.source_image_reference)}
