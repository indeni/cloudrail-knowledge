from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType

class ResourceType(str, Enum):
    VMSS = 'vmss'
    VM = 'vm'


class AzureVirtualMachineExtension(AzureResource):
    """
        Attributes:
            name: The name for the Virtual Machine Scale Set Extension
            publisher: Specifies the Publisher of the Extension
            extension_type: Specifies the type of the Extension
            type_handler_version: Specifies the version of the extension to use
            attached_resource_id: The ID of the Virtual Machine Scale Set or the Virtual Machine which this extnesion config relates to.
    """

    def __init__(self,
                 name: str,
                 publisher: str,
                 extension_type: str,
                 type_handler_version: str,
                 attached_resource_id: str,
                 resource_attached_type: ResourceType):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_MACHINE_EXTENSION)
        self.name: str = name
        self.publisher: str = publisher
        self.extension_type: str = extension_type
        self.type_handler_version: str = type_handler_version
        self.attached_resource_id: str = attached_resource_id
        self.resource_attached_type: ResourceType = resource_attached_type

    def get_cloud_resource_url(self) -> Optional[str]:
        if self.resource_attached_type == ResourceType.VMSS:
            return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
                f'{self.resource_group_name}/providers/Microsoft.Compute/virtualMachineScaleSets/{self.attached_resource_id}/extensions'
        else:
            return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
                f'{self.resource_group_name}/providers/Microsoft.Compute/virtualMachine/{self.attached_resource_id}/extensions'

    @property
    def is_tagable(self) -> bool:
        return self.resource_attached_type == ResourceType.VM

    @staticmethod
    def is_standalone() -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_type(self, is_plural: bool = False) -> str:
        return 'Virtual Machine Scale Set ' + ('Extension' if not is_plural else 'Extensions')

    def get_name(self) -> str:
        return self.name

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags,
                'type_handler_version': self.type_handler_version}
