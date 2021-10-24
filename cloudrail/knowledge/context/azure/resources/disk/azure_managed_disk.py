from enum import Enum
from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType

class StorageAccountType(Enum):
    STANDARD_LRS = 'Standard_LRS'
    PREMIUM_LRS = 'Premium_LRS'
    STANDARDSSD_LRS = 'StandardSSD_LRS'
    ULTRASSD_LRS = 'UltraSSD_LRS'


class ManagedDiskCreateOption(Enum):
    IMPORT = 'Import'
    EMPTY = 'Empty'
    COPY = 'Copy'
    FROMIMAGE = 'FromImage'
    RESTORE = 'Restore'


class AzureManagedDisk(AzureResource):
    """
        Attributes:
            name: The Managed Disk name
            storage_account_type: The type of storage used for the Managed Disk
            create_option: The method used to create the Managed Disk
            disk_encryption_set_id: The ID of the Disk Encryption Set which is being used to encrypt the Managed Disk if any
            disk_encryption_enabled: Indication if the Managed Disk is encrypted using platform key.
    """
    def __init__(self, name: str, storage_account_type: StorageAccountType,
                 create_option: ManagedDiskCreateOption, disk_encryption_set_id: Optional[str], disk_encryption_enabled: bool):
        super().__init__(AzureResourceType.AZURERM_MANAGED_DISK)
        self.name: str = name
        self.storage_account_type: StorageAccountType = storage_account_type
        self.create_option: ManagedDiskCreateOption = create_option
        self.disk_encryption_set_id: Optional[str] = disk_encryption_set_id
        self.disk_encryption_enabled: bool = disk_encryption_enabled

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_type(self, is_plural: bool = False) -> str:
        return 'Managed ' + 'Disk' if not is_plural else 'Disks'

    def get_name(self) -> str:
        return self.name

    @property
    def is_encrypted(self) -> bool:
        return self.disk_encryption_enabled or self.disk_encryption_set_id

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'storage_account_type': self.storage_account_type.value,
                'create_option': self.create_option.value,
                'disc_encryption_set_id': self.disk_encryption_set_id,
                'disc_encryption_enabled': self.disk_encryption_enabled}
