from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureSqlServer(AzureResource):
    """
        Attributes:
            server_name: The name of the SQL server
            public_network_access_enable: An indication on if public network access is enabled.
    """

    def __init__(self, server_name: str, public_network_access_enable: bool) -> None:
        super().__init__(AzureResourceType.AZURERM_SQL_SERVER)
        self.server_name: str = server_name
        self.with_aliases(server_name)
        self.public_network_access_enable: bool = public_network_access_enable

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.server_name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return False
