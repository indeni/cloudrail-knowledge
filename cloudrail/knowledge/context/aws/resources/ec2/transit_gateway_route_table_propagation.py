from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_vpc_attachment import TransitGatewayVpcAttachment


class TransitGatewayRouteTablePropagation(AwsResource):
    """
        Attributes:
            tgw_attachment_id: The TGW attachment ID.
            tgw_route_table_id: The ID of the route table attached.
            attachment: The actual attachment.
    """

    def __init__(self, tgw_attachment_id: str, tgw_route_table_id: str, region: str, account: str):
        super().__init__(account, region, AwsServiceName.AWS_TRANSIT_GATEWAY_ROUTE_TABLE_PROPAGATION)
        self.tgw_attachment_id: str = tgw_attachment_id
        self.tgw_route_table_id: str = tgw_route_table_id
        self.attachment: TransitGatewayVpcAttachment = None

    def get_keys(self) -> List[str]:
        return [self.tgw_attachment_id, self.tgw_route_table_id]

    def get_extra_data(self) -> str:
        tgw_attachment_id = 'tgw_attachment_id: {}'.format(self.tgw_attachment_id) if self.tgw_attachment_id else ''
        tgw_route_table_id = 'tgw_route_table_id: {}'.format(self.tgw_route_table_id) if self.tgw_route_table_id else ''

        return ', '.join([tgw_attachment_id, tgw_route_table_id])

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#TransitGatewayRouteTables:transitGatewayRouteTableId={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.tgw_route_table_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'tgw_attachment_id': self.tgw_attachment_id,
                'tgw_route_table_id': self.tgw_route_table_id}
