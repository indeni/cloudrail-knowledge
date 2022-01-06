from typing import Optional, List
from enum import Enum
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource


class AzureLoadBalancerProbeProtocol(str, Enum):
    HTTP = 'Http'
    HTTPS = 'Https'
    TCP = 'Tcp'


class AzureLoadBalancerProbe(AzureResource):
    """
        Attributes:
            name: Specifies the name of the Probe.
            loadbalancer_id: The ID of the Load Balancer in which to create the Probe.
            protocol: The protocol for the endpoint.
            port: Port on which the Probe queries the backend endpoint.
            request_path: The URI used for requesting health status from the backend endpoint.
            interval_in_seconds: The interval in seconds between probes to the backend endpoint for health status.
            number_of_probes: The number of failed probe attempts after which the backend endpoint is removed from rotation.
    """

    def __init__(self,
                 name: str,
                 loadbalancer_id: str,
                 protocol: AzureLoadBalancerProbeProtocol,
                 port: int,
                 request_path: Optional[str],
                 interval_in_seconds: int,
                 number_of_probes: int):
        super().__init__(AzureResourceType.AZURERM_LB_PROBE)
        self.name: str = name
        self.protocol: AzureLoadBalancerProbeProtocol = protocol
        self.port: int = port
        self.request_path: Optional[str] = request_path
        self.interval_in_seconds: int = interval_in_seconds
        self.number_of_probes: int = number_of_probes
        self.loadbalancer_id: str = loadbalancer_id

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Network/loadBalancers/{self.name}/probes'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Load Balancer Probe' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {'protocol': self.protocol,
                'port': self.port,
                'request_path': self.request_path,
                'interval_in_seconds': self.interval_in_seconds,
                'number_of_probes': self.number_of_probes}
