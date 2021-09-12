from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_resource_type import TransitGatewayResourceType


class TransitGatewayVpcAttachment(AwsResource):
    """
        Attributes:
            attachment_id: The ID of the attachment.
            state: The state of the attachment, one of pending | failing | failed
                | available | deleting | deleted |m odifying | rolling-back.
            resource_type: The type of the resource attached.
            resource_id: The ID of the resource attached.
            name: The name of the attachment.
            subnet_ids: The IDs of the subnets attached to the transit gateway.
    """
    def __init__(self, attachment_id: str, state: str, resource_type: TransitGatewayResourceType, resource_id: str,
                 name: str, subnet_ids: List[str], region: str, account: str):
        super().__init__(account, region, AwsServiceName.AWS_TRANSIT_GATEWAY_ATTACHMENT)
        self.attachment_id: str = attachment_id
        self.state: str = state
        self.resource_type: TransitGatewayResourceType = resource_type
        self.resource_id: str = resource_id
        self.name: str = name
        self.subnet_ids: List[str] = subnet_ids

    def get_keys(self) -> List[str]:
        return [self.attachment_id]

    def get_extra_data(self) -> str:
        tgw_attachment_id = 'tgw_attachment_id: {}'.format(self.attachment_id) if self.attachment_id else ''
        subnet_ids = 'subnet_ids: {}'.format(self.subnet_ids) if self.subnet_ids else ''

        return ', '.join([tgw_attachment_id, subnet_ids])

    def get_id(self) -> str:
        return self.attachment_id

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#TransitGatewayAttachments:transitGatewayAttachmentId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.attachment_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
