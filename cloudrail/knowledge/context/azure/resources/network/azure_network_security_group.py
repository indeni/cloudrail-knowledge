from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group_rule import AzureNetworkSecurityRule


class AzureNetworkSecurityGroup(AzureResource):
    """
        Attributes:
            name: The network security group name.
            subnets: List of subnets which the network security group is connected to.
            network_interfaces: List of actual network interfaces which the network security group is connected to.
            network_security_rules: The rules that are assigned to this network security group.
    """

    def __init__(self,
                 name: str,
                 network_security_rules: List[AzureNetworkSecurityRule]):
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.name: str = name
        self.network_security_rules: List[AzureNetworkSecurityRule] = network_security_rules

        self.subnets: List['AzureSubnet'] = []
        self.network_interfaces: List['AzureNetworkInterface'] = []

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Network/networkSecurityGroups/{self.name}/overview'

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True

    def exclude_from_invalidation(self) -> list:
        return [self.subnets, self.network_interfaces]

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'network_security_rules': self.network_security_rules and
                                          [rules.to_drift_detection_object() for rules in self.network_security_rules]}
