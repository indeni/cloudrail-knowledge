from enum import Enum


class TransitGatewayResourceType(Enum):
    VPC = 'vpc'
    VPN = 'vpn'
    PEERING = 'peering'
