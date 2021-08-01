from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType

class NetworkRuleDefaultAction(Enum):
    """
        Enum

        ALLOW - Default Action is set to Allow connections
        DENY - Default Action is set to Deny connections
    """
    ALLOW = 'allow'
    DENY = 'deny'


class BypassTrafficType(Enum):
    NONE = 'none'
    LOGGING = 'Logging'
    METRICS = 'Metrics'
    AZURESERVICES = 'AzureServices'

class AzureStorageAccountNetworkRules(AzureResource):
    """
        Attributes:
            storage_name: The name of the storage account.
            default_action: The default action when no other rules match.
            ip_rules: List of IP addresses to allow access from the internet to the storage account.
            bypass_traffic: List of traffic services which will bypass the network rules, and will have access to the storage account.
    """

    def __init__(self, storage_name: str, default_action: str, ip_rules: list, bypass_traffic: list) -> None:
        super().__init__(AzureResourceType.AZURERM_STORAGE_ACCOUNT_NETWORK_RULES)
        self.storage_name: str = storage_name
        self.with_aliases(storage_name)
        self.default_action: NetworkRuleDefaultAction = default_action
        self.ip_rules: list = ip_rules
        self.bypass_traffic: List[BypassTrafficType] = bypass_traffic

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.storage_name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self.get_id()}/networking'

    def get_friendly_name(self) -> str:
        return 'Network rule for Storage account' + self.get_name()

    def get_type(self, is_plural: bool = False) -> str:
        return 'Storage account network ' + 'rule' if not is_plural else 'rules'

    @property
    def is_tagable(self) -> bool:
        return False

    @staticmethod
    def is_standalone() -> bool:
        return False
