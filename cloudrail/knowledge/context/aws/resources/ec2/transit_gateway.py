from typing import List

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table import TransitGatewayRouteTable
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class TransitGateway(AwsResource):
    """
        Attributes:
            name: The name of the Transit Gateway.
            tgw_id: The Transit Gateway's ID.
            state: The state of the TGW, one of available | deleted | deleting | modifying | pending.
            route_tables: The routing tables connected to this transit gateway.
    """

    def __init__(self, name: str, tgw_id: str, state: str, region: str, account: str):
        super().__init__(account, region, AwsServiceName.AWS_TRANSIT_GATEWAY)
        self.name: str = name
        self.tgw_id: str = tgw_id
        self.state: str = state
        self.route_tables: List[TransitGatewayRouteTable] = []
        self.with_aliases(self.tgw_id)

    def get_keys(self) -> List[str]:
        return [self.tgw_id]

    def get_id(self) -> str:
        return self.tgw_id

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#TransitGateways:transitGatewayId={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.tgw_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'name': self.name,
                'state': self.state}
