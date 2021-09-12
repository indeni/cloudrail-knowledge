from typing import Dict
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_vpc_link import ApiGatewayVpcLink
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationApiGatewayV2VpcLinkBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.API_GATEWAY_V2_VPC_LINK, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> ApiGatewayVpcLink:
        properties: dict = cfn_res_attr['Properties']
        return ApiGatewayVpcLink(account=cfn_res_attr['account_id'],
                                 region=cfn_res_attr['region'],
                                 vpc_link_id=self.get_resource_id(cfn_res_attr),
                                 name=self.get_property(properties, 'Name'),
                                 arn=None,
                                 security_group_ids=self.get_property(properties, 'SecurityGroupIds'),
                                 subnet_ids=self.get_property(properties, 'SubnetIds'))
