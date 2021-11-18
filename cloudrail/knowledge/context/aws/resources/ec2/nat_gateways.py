from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.utils.tags_utils import filter_tags


class NatGateways(NetworkEntity):
    """
        Attributes:
            nat_gateway_id: The ID of this NAT gateway.
            allocation_id: The allocation ID used with this NAT gateway.
            subnet_id: The subnet the NAT is tired to.
            eni_id: The elastic network interface the NAT gateway is tied to.
            private_ip: The private IP of the NAT gateway.
            public_ip: The public IP of the NAT gateway.
    """

    def __init__(self, nat_gateway_id: str, allocation_id: str, subnet_id: str, eni_id: str,
                 private_ip: str, public_ip: str, account: str, region: str):
        super().__init__(nat_gateway_id, account, region, AwsServiceName.AWS_NAT_GATEWAY)
        self.nat_gateway_id: str = nat_gateway_id
        self.allocation_id: str = allocation_id
        self.with_aliases(nat_gateway_id)
        self.subnet_id: str = subnet_id
        self.eni_id: str = eni_id
        self.private_ip: str = private_ip
        self.public_ip: str = public_ip

    def get_keys(self) -> List[str]:
        return [self.nat_gateway_id]

    def get_id(self) -> str:
        return self.nat_gateway_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'NAT gateway'
        else:
            return 'NAT gateways'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#NatGatewayDetails:natGatewayId={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.nat_gateway_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'allocation_id': self.allocation_id,
                'subnet_id': self.subnet_id}
