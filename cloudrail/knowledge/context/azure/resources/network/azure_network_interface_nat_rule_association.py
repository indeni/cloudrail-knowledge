from typing import Optional, List
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource


class AzureNetworkInterfaceNatRuleAssociation(AzureResource):
    """
        Attributes:
            ip_configuration_name: The name of the IP Configuration within the Network Interface which should be connected to the NAT rule.
            network_interface_id: The ID of the Network Interface.
            nat_rule_id: The ID of the Load Balancer NAT Rule which this Network Interface should be connected to.
    """

    def __init__(self,
                 ip_configuration_name: str,
                 network_interface_id: str,
                 nat_rule_id: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_INTERFACE_NAT_RULE_ASSOCIATION)
        self.ip_configuration_name: str = ip_configuration_name
        self.network_interface_id: str = network_interface_id
        self.nat_rule_id: str = nat_rule_id

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.network_interface_id, self.nat_rule_id, self.ip_configuration_name]

    @staticmethod
    def is_standalone() -> bool:
        return False

    def get_type(self, is_plural: bool = False) -> str:
        return 'Network Interface NAT Rule Association' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {}
