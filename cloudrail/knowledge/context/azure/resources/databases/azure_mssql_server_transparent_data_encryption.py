from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class AzureMsSqlServerTransparentDataEncryption(AzureResource):
    """
        Attributes:
            server_id: Specifies the name or ID of the MS SQL Server.
            key_vault_key_id: To use customer managed keys from Azure Key Vault, provide the AKV Key ID. To use service managed keys, omit this field.
    """

    def __init__(self,
                 server_id: str,
                 key_vault_key_id: Optional[str]):
        super().__init__(AzureResourceType.AZURERM_MSSQL_SERVER_TRANSPARENT_DATA_ENCRYPTION)
        self.server_id: str = server_id
        self.key_vault_key_id: Optional[str] = key_vault_key_id

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> Optional[str]:
        return f'SQL server transparent data encryption of server {self.server_id}'

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    @staticmethod
    def is_standalone() -> bool:
        return False

    def get_type(self, is_plural: bool = False) -> str:
        return 'Azure SQL server transparent data encryption ' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {'key_vault_key_id': self.key_vault_key_id}
