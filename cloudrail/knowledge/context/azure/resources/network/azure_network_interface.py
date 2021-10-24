from typing import List, Optional

from cloudrail.knowledge.context.connection import ConnectionInstance
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.network.azure_application_security_group import AzureApplicationSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_public_ip import AzurePublicIp
from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet


class IpConfiguration(ConnectionInstance):
    """
        Attributes:
            public_ip_id: The ID of the PublicIp resource that's attached to this IP Configuration resource.
            public_ip: The actual PublicIp resource that's attached to this IP Configuration resource.
            subnet_id: The ID of the Subnet that this IP Configuration resource is attached to.
            subnet: The actual Subnet that this IP Configuration resource is attached to.
            private_ip: The private ip address of this IP Configuration.
            application_security_groups_ids: List of ASG's id's that's attached to this IP Configuration resource.
            application_security_groups: List of actual ASG's that's attached to this IP Configuration resource.
    """

    def __init__(self, public_ip_id: str, subnet_id: str, private_ip: Optional[str], application_security_groups_ids: List[str]):
        ConnectionInstance.__init__(self)
        self.public_ip_id: str = public_ip_id
        self.subnet_id: str = subnet_id
        self.private_ip: Optional[str] = private_ip
        self.application_security_groups_ids: List[str] = application_security_groups_ids

        self.application_security_groups: List[AzureApplicationSecurityGroup] = []
        self.public_ip: AzurePublicIp = None
        self.subnet: AzureSubnet = None

    def to_dict(self):
        return {'public_ip_id': self.public_ip_id,
                'subnet_id': self.subnet_id,
                'private_ip': self.private_ip,
                'application_security_groups_ids': self.application_security_groups_ids}


class AzureNetworkInterface(AzureResource):
    """
        Attributes:
            name: The name of this network interface.
            network_security_group: The security group that's attached to this network interface.
            ip_configurations: IP configurations of a network interface.
    """

    def __init__(self, name: str, ip_configurations: List[IpConfiguration], network_security_group_id: Optional[str] = None):
        AzureResource.__init__(self, AzureResourceType.AZURERM_NETWORK_INTERFACE)
        self.name: str = name
        self.ip_configurations: List[IpConfiguration] = ip_configurations

        self.network_security_group: Optional[AzureNetworkSecurityGroup] = None
        self._network_security_group_id: Optional[str] = network_security_group_id

    @property
    def network_security_group_id(self):
        return self._network_security_group_id or (self.network_security_group and self.network_security_group.get_id())

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Network/networkInterfaces/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    @property
    def inbound_connections(self):
        return {inbound_connection for ip_config in self.ip_configurations for inbound_connection in ip_config.inbound_connections}

    @property
    def outbound_connections(self):
        return {outbound_connection for ip_config in self.ip_configurations for outbound_connection in ip_config.outbound_connections}

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'ip_configurations': [config.to_dict() for config in self.ip_configurations],
                'network_security_group_id': self.network_security_group_id}
