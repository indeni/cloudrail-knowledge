from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_resource_type import TransitGatewayResourceType
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_vpc_attachment import TransitGatewayVpcAttachment
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationTransitGatewayAttachmentBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.TRANSIT_GATEWAY_ATTACHMENT, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> TransitGatewayVpcAttachment:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account_id = cfn_res_attr['account_id']
        return TransitGatewayVpcAttachment(transit_gateway_id=self.get_property(properties, 'TransitGatewayId'),
                                           attachment_id=self.get_resource_id(cfn_res_attr),
                                           state=None,
                                           resource_type=TransitGatewayResourceType.VPC,
                                           resource_id=self.get_property(properties, 'VpcId'),
                                           name=self.get_name_tag(properties),
                                           subnet_ids=self.get_property(properties, 'SubnetIds'),
                                           region=region,
                                           account=account_id)
