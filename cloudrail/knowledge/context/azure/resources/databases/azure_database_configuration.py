from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureDatabaseConfiguration(AzureResource):
    """
        Attributes:
            name: Specifies the name of the DB Configuration
            value: Specifies the value of the DB Configuration.
            server_name: Specifies the name of the DB Server
    """

    def __init__(self, name: str, value: str, server_name: str) -> None:
        super().__init__(AzureResourceType.AZURERM_POSTGRESQL_CONFIGURATION)  # TODO: how to make it more generic , talk with Tomer
        self.name: str = name
        self.value: str = value
        self.server_name: str = server_name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        pass

    def is_standalone(self) -> bool:
        return False
