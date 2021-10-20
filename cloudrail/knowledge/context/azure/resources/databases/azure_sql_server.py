from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import \
    AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import \
    AzureSqlServerExtendedAuditingPolicy


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
        self.extended_auditing_policy: AzureSqlServerExtendedAuditingPolicy = None

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.server_name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'server_name': self.server_name,
                'public_network_access_enabled': self.public_network_access_enable}
