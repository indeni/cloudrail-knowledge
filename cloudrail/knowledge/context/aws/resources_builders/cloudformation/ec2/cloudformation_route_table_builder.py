from typing import Dict
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationRouteTable(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ROUTE_TABLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> RouteTable:
        properties: dict = cfn_res_attr['Properties']
        return RouteTable(route_table_id=self.get_resource_id(cfn_res_attr),
                          vpc_id=self.get_property(properties, 'VpcId'),
                          name=self.get_name_tag(properties),
                          region=cfn_res_attr['region'],
                          account=cfn_res_attr['account_id'],
                          is_main_route_table=False)
