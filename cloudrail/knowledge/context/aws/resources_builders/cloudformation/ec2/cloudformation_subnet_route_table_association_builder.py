from typing import Dict
from cloudrail.knowledge.context.aws.resources.ec2.route_table_association import RouteTableAssociation
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationSubnetRouteTableAssociationBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.SUBNET_ROUTE_TABLE_ASSOCIATION, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> RouteTableAssociation:
        properties: dict = cfn_res_attr['Properties']
        return RouteTableAssociation(association_id=self.get_resource_id(cfn_res_attr),
                                     subnet_id=self.get_property(properties, 'SubnetId'),
                                     route_table_id=self.get_property(properties, 'RouteTableId'),
                                     region=cfn_res_attr['region'],
                                     account=cfn_res_attr['account_id'])
