from typing import Dict
from cloudrail.knowledge.context.aws.resources.ec2.vpc_gateway_attachment import VpcGatewayAttachment
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationVpcGatewayAttachmentBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.VPC_GATEWAY_ATTACHMENT, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> VpcGatewayAttachment:
        properties: dict = cfn_res_attr['Properties']
        return VpcGatewayAttachment(vpc_id=self.get_property(properties, 'VpcId'),
                                    gateway_id=self.get_property(properties, 'InternetGatewayId') or
                                               self.get_property(properties, 'VpnGatewayId'),
                                    region=cfn_res_attr['region'],
                                    account=cfn_res_attr['account_id'])
