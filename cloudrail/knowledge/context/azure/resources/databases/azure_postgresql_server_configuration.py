from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzurePostgreSqlServerConfiguration(AzureResource):
    """
        Attributes:
            name: Specifies the name of the PostgreSQL Configuration, which needs to be a valid PostgreSQL configuration name.
            server_name: Specifies the name of the PostgreSQL Server.
            value: Specifies the value of the PostgreSQL Configuration.
    """

    def __init__(self,
                 name: str,
                 server_name: str,
                 value: str):
        super().__init__(AzureResourceType.AZURERM_POSTGRESQL_SERVER_CONFIGURATION)
        self.name: str = name
        self.server_name: str = server_name
        self.value: str = value

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.DBforPostgreSQL/servers/{self.server_name}/serverParameters'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'PostgreSQL Server Configuration' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {'server_name': self.server_name,
                'value': self.value}
