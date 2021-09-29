from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureMySqlServer(AzureResource):
    """
        Attributes:
            server_name: The name of the SQL server
            ssl_enforcement_enabled: An indication on if ssl enforcement is enabled.
    """

    def __init__(self, server_name: str, ssl_enforcement_enabled: bool) -> None:
        super().__init__(AzureResourceType.AZURERM_MYSQL_SERVER)
        self.server_name: str = server_name
        self.with_aliases(server_name)
        self.ssl_enforcement_enabled: bool = ssl_enforcement_enabled

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.server_name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/' \
               f'Microsoft.DBForMySQL/servers/{self.server_name}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'MySQL Server'
        else:
            return 'MySQL Servers'

    @property
    def is_tagable(self) -> bool:
        return True
