from typing import Optional, List
from enum import Enum

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource


class AzureLoadBalancerNatRuleProtocol(str, Enum):
    UDP = 'udp'
    TCP = 'tcp'
    ALL = 'all'


class AzureLoadBalancerNatRule(AzureResource):
    """
        Attributes:
            name: The name of the NAT Rule.
            loadbalancer_id: The ID of the Load Balancer in which to create the NAT rule.
            frontend_ip_configuration_name: The name of the frontend IP configuration exposing this rule.
            protocol: The transport protocol for the external endpoint.
            frontend_port: The port for the external endpoint.
            backend_port: The port used for internal connections on the endpoint.
            idle_timeout_in_minutes: Specifies the idle timeout in minutes for TCP connections.
            enable_floating_ip: To enable floating IPs for this Load Balancer rule.
            enable_tcp_reset: To enable TCP Reset for this Load Balancer rule.
    """

    def __init__(self,
                 name: str,
                 loadbalancer_id: str,
                 frontend_ip_configuration_name: str,
                 protocol: AzureLoadBalancerNatRuleProtocol,
                 frontend_port: int,
                 backend_port: int,
                 idle_timeout_in_minutes: int,
                 enable_floating_ip: bool,
                 enable_tcp_reset: bool):
        super().__init__(AzureResourceType.AZURERM_LB_NAT_RULE)
        self.name: str = name
        self.frontend_ip_configuration_name: str = frontend_ip_configuration_name
        self.protocol: AzureLoadBalancerNatRuleProtocol = protocol
        self.frontend_port: int = frontend_port
        self.backend_port: int = backend_port
        self.idle_timeout_in_minutes: int = idle_timeout_in_minutes
        self.enable_floating_ip: bool = enable_floating_ip
        self.enable_tcp_reset: bool = enable_tcp_reset
        self.loadbalancer_id: str = loadbalancer_id

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Network/loadBalancers/{self.name}/inboundNatRules'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Load Balancer NAT Rule' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {
            'frontend_ip_configuration_name': self.frontend_ip_configuration_name,
            'protocol': self.protocol,
            'frontend_port': self.frontend_port,
            'backend_port': self.backend_port,
            'idle_timeout_in_minutes': self.idle_timeout_in_minutes,
            'enable_floating_ip': self.enable_floating_ip,
            'enable_tcp_reset': self.enable_tcp_reset,
            'loadbalancer_id': self.loadbalancer_id
        }
