from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationTransitGatewayBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.TRANSIT_GATEWAY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> TransitGateway:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account_id = cfn_res_attr['account_id']
        return TransitGateway(self.get_name_tag(properties),
                              self.get_resource_id(cfn_res_attr),
                              None, region, account_id)
