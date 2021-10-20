from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_resource_type import TransitGatewayResourceType


class TransitGatewayRouteAttachment(AwsResource):
    """
        Attributes:
            tgw_id: The Transit Gateway the route is to be attached to.
            resource_type: The type of the resource attached to the TGW.
            resource_id: The ID of the resource attached to the TGW.
    """

    def __init__(self,
                 tgw_id: str,
                 resource_type: TransitGatewayResourceType,
                 resource_id: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.NONE)
        self.tgw_id: str = tgw_id
        self.resource_type: TransitGatewayResourceType = resource_type
        self.resource_id: str = resource_id

    def get_keys(self) -> List[str]:
        return [self.tgw_id, self.resource_id]

    def get_extra_data(self) -> str:
        tgw_id = 'tgw_id: {}'.format(self.tgw_id) if self.tgw_id else ''
        resource_type = 'resource_type: {}'.format(self.resource_type) if self.resource_type else ''
        resource_id = 'resource_id: {}'.format(self.resource_id) if self.resource_id else ''

        return ', '.join([tgw_id, resource_type, resource_id])

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#TransitGateways:transitGatewayId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.tgw_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'tgw_id': self.tgw_id,
                'resource_type': self.resource_type.value,
                'resource_id': self.resource_id}
