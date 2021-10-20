from typing import Dict
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import IntegrationType
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import RestApiMethod
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_integration import ApiGatewayV2Integration
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationApiGatewayV2IntegrationBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.API_GATEWAY_V2_INTEGRATION, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> ApiGatewayV2Integration:
        properties: dict = cfn_res_attr['Properties']
        return ApiGatewayV2Integration(account=cfn_res_attr['account_id'],
                                       region=cfn_res_attr['region'],
                                       rest_api_id=self.get_property(properties, 'ApiId'),
                                       connection_id=self.get_property(properties, 'ConnectionId'),
                                       integration_id=self.get_resource_id(cfn_res_attr),
                                       integration_http_method=RestApiMethod(self.get_property(properties, 'IntegrationMethod')),
                                       integration_type=IntegrationType(self.get_property(properties, 'IntegrationType')),
                                       uri=self.get_property(properties, 'IntegrationUri'))
