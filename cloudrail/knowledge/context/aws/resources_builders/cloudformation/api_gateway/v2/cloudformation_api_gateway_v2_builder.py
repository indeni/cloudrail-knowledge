from typing import Dict
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2 import ApiGateway
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationApiGatewayV2Builder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.API_GATEWAY_V2, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> ApiGateway:
        properties: dict = cfn_res_attr['Properties']
        return ApiGateway(account=cfn_res_attr['account_id'],
                          region=cfn_res_attr['region'],
                          api_gw_id=self.get_resource_id(cfn_res_attr),
                          api_gw_name=self.get_property(properties, 'Name'),
                          protocol_type=self.get_property(properties, 'ProtocolType'),
                          arn=self.get_property(properties, 'Target'))
