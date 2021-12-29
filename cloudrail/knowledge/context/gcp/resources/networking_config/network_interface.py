from typing import List, Optional
from enum import Enum
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork

class GcpComputeInstanceNetIntfNicType(str, Enum):
    GVNIC  = 'gvnic'
    VIRTIO_NET = 'virtio_net'

class GcpNetworkInterface:
    """
        Represents a network interface that can be assigned to a specific
        network-bound resource, such as compute_instance.

        Attributes:
            network: The name or self_link of the network to attach this interface to.
            private_ip: The internal private IP of the interface, used for internal communication between GCP resources.
            public_ips: List of public IP's assigned to the interface.
            nic_type: The type of vNIC to be used on this interface. Possible values: GVNIC, VIRTIO_NET.
    """

    def __init__(self,
                 network: str,
                 private_ip: Optional[str],
                 public_ips: Optional[list],
                 nic_type: GcpComputeInstanceNetIntfNicType):
        self.network: str = network
        self.private_ip: Optional[str] = private_ip
        self.public_ips: Optional[list] = public_ips
        self.nic_type: GcpComputeInstanceNetIntfNicType = nic_type
        self.vpc_network: GcpComputeNetwork = None
        self.firewalls: List[GcpComputeFirewall] = None
