from typing import Dict

from cloudrail.knowledge.context.aws.resources.rds.db_subnet_group import DbSubnetGroup
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationRdsDbSubnetGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.RDS_DB_SUBNET_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> DbSubnetGroup:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        name = self.get_property(properties, 'DBSubnetGroupName', self.get_resource_id(cfn_res_attr))
        db_subnet_group_arn = build_arn('rds', region, account, 'subgrp', None, name)
        return DbSubnetGroup(account=account,
                             region=region,
                             name=self.get_property(properties, 'DBSubnetGroupName', self.get_resource_id(cfn_res_attr)),
                             subnet_ids=self.get_property(properties, 'SubnetIds'),
                             db_subnet_group_arn=db_subnet_group_arn)
